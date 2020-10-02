#라즈베리파이 Python 코드
#블루투스 통신을 위한 전역변수 선언
passwordbool = False
btSerial = serial.Serial("/dev/rfcomm0", baudrate=115200)
blueSerial100 = '0'





    def __init__(self):
        self.interrupted=False
        self.can_start_conversation=False
        self.assistant=None
        self.sensitivity = [0.5]*len(models)
        self.callbacks = [self.detected]*len(models)
        self.detector = snowboydecoder.HotwordDetector(models, sensitivity=self.sensitivity)
        self.t1 = Thread(target=self.start_detector)
        self.t2 = Thread(target=self.pushbutton)
        
        #아두이노신호를 받아오는 쓰레드추가
        self.tttt = Thread(target=self.blue)






    def process_event(self,event):
        """Pretty prints events.
        Prints all events that occur with two spaces between each new
        conversation and a single space between turns of a conversation.
        Args:
            event(event.Event): The current event to process.
        """
        print(event)
        if event.type == EventType.ON_START_FINISHED:
            self.can_start_conversation = True
            self.t2.start()

            self.tttt.start()


    #아두이노로 부터 습도, 가스, 움직임감지 신호를 받아서 처리하는 함수
    def blue(self):
        global blueSerial100
        global btSerial
        while True:
            blueSerial100 = btSerial.readline()

            if blueSerial100 == 'PANON1': #아두이노로부터 pan을 작동시키라는 신호를 받음
                 say("Pan on")
            elif blueSerial100 == 'PANOFF1': #아두이노로부터 pan을 정지시키라는 신호를 받음
                 say("Pan off")
            elif blueSerial100 == 'GAS': #아두이노로부터 GAS를 감지했다는 신호를 받음
                 say("Gas is detected")
            elif blueSerial100 == 'PASSWORD': #아두이노로부터 움직임을 감지했다는 신호를 받음
                 event.type = EventType.ON_CONVERSATION_TURN_STARTED
                 global passwordbool
                 passwordbool = True
                 say("Please say password")
            elif blueSerial100 >= '10000' and blueSerial100 <= '10100': #아두이노로부터 습도가 몇인지 받음
                 say(btSerial.readline() - '10000')


    def main(self):
        global passwordbool
        global btSerial
        global blueSerial100
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--device-model-id', '--device_model_id', type=str,
                            metavar='DEVICE_MODEL_ID', required=False,
                            help='the device model ID registered with Google')
        parser.add_argument('--project-id', '--project_id', type=str,
                            metavar='PROJECT_ID', required=False,
                            help='the project ID used to register this device')
        parser.add_argument('--device-config', type=str,
                            metavar='DEVICE_CONFIG_FILE',
                            default=os.path.join(
                                os.path.expanduser('~/.config'),
                                'googlesamples-assistant',
                                'device_config_library.json'
                            ),
                            help='path to store and read device configuration')
        parser.add_argument('--credentials', type=existing_file,
                            metavar='OAUTH2_CREDENTIALS_FILE',
                            default=os.path.join(
                                os.path.expanduser('~/.config'),
                                'google-oauthlib-tool',
                                'credentials.json'
                            ),
                            help='path to store and read OAuth2 credentials')
        parser.add_argument('-v', '--version', action='version',
                            version='%(prog)s ' + Assistant.__version_str__())

        args = parser.parse_args()
        with open(args.credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))

        device_model_id = None
        last_device_id = None
        try:
            with open(args.device_config) as f:
                device_config = json.load(f)
                device_model_id = device_config['model_id']
                last_device_id = device_config.get('last_device_id', None)
        except FileNotFoundError:
            pass

        if not args.device_model_id and not device_model_id:
            raise Exception('Missing --device-model-id option')

         Re-register if "device_model_id" is given by the user and it differs
         from what we previously registered with.
        should_register = (
            args.device_model_id and args.device_model_id != device_model_id)

        device_model_id = args.device_model_id or device_model_id
        with Assistant(credentials, device_model_id) as assistant:
            self.assistant = assistant
            subprocess.Popen(["aplay", "{}/sample-audio-files/Startup.wav".format(ROOT_PATH)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            events = assistant.start()
            device_id = assistant.device_id
            print('device_model_id:', device_model_id)
            print('device_id:', device_id + '\n')

            # Re-register if "device_id" is different from the last "device_id":
            if should_register or (device_id != last_device_id):
                if args.project_id:
                    register_device(args.project_id, credentials,
                                    device_model_id, device_id)
                    pathlib.Path(os.path.dirname(args.device_config)).mkdir(
                        exist_ok=True)
                    with open(args.device_config, 'w') as f:
                        json.dump({
                            'last_device_id': device_id,
                            'model_id': device_model_id,
                        }, f)
                else:
                    print(WARNING_NOT_REGISTERED)

            # Google Assistant API에 "pan off", "humidity" event 추가
            # pan off event를 받으면, pan off라고 응답
            # humidity event를 받으면, 현재 습도를 응답
            for event in events:
                self.process_event(event)
                usrcmd=event.args
                if passwordbool:
                    if 'password'.lower() in str(usrcmd).lower():
                        assistant.stop_conversation()
                        PASSWORD1(str(usrcmd).lower())
                        passwordbool = False
                    else:
                        assistant.stop_conversation()
                        PASSWORD2(str(usrcmd).lower())
                        passwordbool = False
                if 'television'.lower() in str(usrcmd).lower():
                    assistant.stop_conversation()
                    #btSerial.write(str.encode(str(usrcmd).lower()))
                    TELEVISION(str(usrcmd).lower())
                if 'pan off'.lower() in str(usrcmd).lower():
                    assistant.stop_conversation()
                    #btSerial.write(str.encode(str(usrcmd).lower()))
                    PANOFF(str(usrcmd).lower())
                if 'humidity'.lower() in str(usrcmd).lower():
                    assistant.stop_conversation()
                    #btSerial.write(str.encode(str(usrcmd).lower()))
                    HUMIDITY(str(usrcmd).lower(), blueSerial100)
