from pygame import mixer

Sound = mixer.Sound
Channel = mixer.Channel

class Audio:

    _instance = None

    def __init__(self):
        self.songs: dict[str, tuple[Channel, Sound]] = {}
    
    def play_song(self, name: str, file_loc: str, looping: bool = False):
        sound: Sound = Sound(file_loc)
        channel: Channel = mixer.find_channel()
        if channel:
            self.songs[name] = (channel, sound)
            channel.play(sound, -1 if looping else 1)
    
    def stop_song(self, name: str):
        if name in self.songs:
            channel: Channel = self.songs[name][0]
            sound: Sound = self.songs[name][1]
            if channel.get_sound() == sound and channel.get_busy():
                channel.stop()
    
    def get_instance():
        if Audio._instance == None:
            mixer.init()
            mixer.set_num_channels(5)
            Audio._instance = Audio()
        return Audio._instance