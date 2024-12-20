def evaluate_tts(cosyvoice_path, whisper_path, dataset, language="yue"):
    import os
    import tqdm
    import evaluate
    from yue_normalizer.tools import han_normalize
    from yue_normalizer.chinese_normalizer import TextNorm
    import torchaudio
    import faster_whisper
    from cosyvoice.cli.cosyvoice import CosyVoice

    cosyvoice = CosyVoice(cosyvoice_path, load_jit=True, load_onnx=False, fp16=True)
    print(cosyvoice.list_avaliable_spks())

    whisper = faster_whisper.WhisperModel(
        model_size_or_path=whisper_path,
    )

    cer_asr = evaluate.load(os.path.join(os.path.dirname(__file__), "cer"))
    cer_tts_asr = evaluate.load(os.path.join(os.path.dirname(__file__), "cer"))

    for one_sample in tqdm.tqdm(dataset):
        transcription = one_sample["raw_transcription"]
        audio = one_sample["audio"]["array"]

        # asr
        def get_asr(audio, language):
            asr_segements, _ = whisper.transcribe(audio, language=language)
            asr_result = "".join([seg.text for seg in asr_segements])
            return asr_result

        asr_result = get_asr(audio, language=language)

        # tts
        def get_tts(text):
            tts_result = list(cosyvoice.inference_sft(text, "粤语女", stream=False))[0][
                "tts_speech"
            ]
            return torchaudio.transforms.Resample(22050, 16000)(tts_result).numpy()[0]

        tts_result = get_tts(transcription)
        tts_asr_result = get_asr(tts_result, language=language)

        text_norm = TextNorm(remove_fillers=True, remove_space=True)

        cer_tts_asr.add(
            reference=text_norm(han_normalize(transcription)),
            prediction=text_norm(han_normalize(tts_asr_result)),
        )
        cer_asr.add(
            reference=text_norm(han_normalize(transcription)),
            prediction=text_norm(han_normalize(asr_result)),
        )

    return cer_tts_asr.compute(), cer_asr.compute()
