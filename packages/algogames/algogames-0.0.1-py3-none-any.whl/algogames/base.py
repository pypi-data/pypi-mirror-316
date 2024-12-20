import json
import sys
import threading
import ctypes
from abc import ABC, abstractmethod


class EngineInterface(ABC):


    def __init__(self, gamestate_class):
        self._gamestate_class = gamestate_class


    def _receive(self) -> dict:
        return json.loads(input())
    

    def _send(self, command: str, data: dict) -> None:
        sys.stdout.write(json.dumps({'command': command, 'data': data}) + '\n')
        sys.stdout.flush()


    def _get_gs(self):
        return self._gamestate_class(self._receive())


    def log(self, msg) -> None:
        self._send('log', {'message': str(msg)})


    def get_time_left(self) -> int:
        self._send('get-time-left', {})
        recieved = self._receive()
        return recieved['time']


    def _run(self, algo_class) -> None:
        algo = algo_class(self, self._parse_config(self._receive()))
        self._send('end-initial-timer', {})
        self._game_loop(algo)


    # overwrite in child class if needed
    def _parse_config(self, config: dict) -> dict:
        return config


    @abstractmethod
    def _game_loop(self, algo) -> None:
        pass


#########################################################################################
# The below classes were meant to allow games like snake and duelsnakes
# to continue even after the algo timed out. Meaning if the algo timed out, 
# the interface would cancel that thread and start it anew with the next tick's info.
# We are abandoning this idea for now due to unnecassary complexity 


class CancellableThread(threading.Thread):

    def __init__(self, func):
        threading.Thread.__init__(self)
        self.run = func
             

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for tid, thread in threading._active.items():
            if thread is self:
                return tid


    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)


    def cancel(self):
        self.raise_exception()
        self.join()


class ThreadedInterface(EngineInterface):

    def __init__(self, gamestate_class):
        super().__init__(gamestate_class)
        self._message_event = threading.Event()
        self._message = None

    @property
    def time_left(self):
        self._send('get-time-left', {})
        
        self._message_event.wait() # up to the run function to set 
        self._message_event.clear()

        return self._message['time']
    
    def _set_message(self, message):
        self._message = message
        self._message_event.set()
