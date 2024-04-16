import torch

device = torch.device('cpu')
local_file = 'model.pt'
model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)


class Speaker:
    def __init__(self):
        torch.set_num_threads(4)
        self.sample_rate = 48000
        self.speaker = 'baya'

    def text_to_spreach(self, example_text):
        audio_paths = model.save_wav(text=example_text,
                                     speaker=self.speaker,
                                     sample_rate=self.sample_rate)


speaker = Speaker()
speaker.text_to_spreach('Алексей тупое чмо и инфантильный пидорас.')