from abc import ABC
from abc import abstractmethod


class BaseInput(ABC):

   def __init__(self):
   	pass

   @abstractmethod
   def __enter__(self):
      pass

   @abstractmethod
   def __exit__(self, type, value, traceback):
   	pass
   
   @abstractmethod
   async def connect_to(self, output):
      pass
