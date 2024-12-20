
try:
    from aria2_kit import aria2_kit
except:    
    from .aria2_kit import aria2_kit
try:
    from s3_kit import s3_kit
except:
    from .s3_kit import s3_kit    
try:
    from websocket_kit import websocket_kit
except:
    from .websocket_kit import websocket_kit

class libp2p_kit:
    def __init__(self, resources=None, metadata=None):
        self.libp2p_kit = libp2p_kit(resources, metadata)
        self.aria2_kit = aria2_kit(resources, metadata)
        self.s3_kit = s3_kit(resources, metadata)
        self.websocket_kit = websocket_kit(resources, metadata)
        pass
    
    def run(self):

        return True
    
    