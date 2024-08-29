class GraphNode:
    def __init__(self, id:str):
        self.id = id

    def __str__(self):
        return self.id

class GraphEdge:
    def __init__(self, id:str):
        self.id = id

    def __str__(self):
        return self.id
    
class GraphAnon:
    def __init__(self, id:str):
        self.id = id

    def __str__(self):
        return self.id

class SimpleDate:
    def __init__(self, year:int, month:int, day:int, tzMinuteOffset:int):
        self.year = year
        self.month = month
        self.day = day
        self.tzMinuteOffset = tzMinuteOffset

    def __str__(self):
        year = str(self.year)
        month = str(self.month).zfill(2)
        day = str(self.day).zfill(2)
        res = f'{year}-{month}-{day}'
        if self.tzMinuteOffset == 0:
            res += 'Z'
        else:
            tzHour = self.tzMinuteOffset // 60
            tzMin = self.tzMinuteOffset % 60
            res += '-' if self.tzMinuteOffset < 0 else '+'
            res += str(abs(tzHour)).zfill(2) + ':'
            res += str(abs(tzMin)).zfill(2)
        return res

class Time:
    def __init__(self, hour:int, minute:int, second:int, millisecond:int, tzMinuteOffset:int):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.millisecond = millisecond
        self.tzMinuteOffset = tzMinuteOffset

    def __str__(self):
        hour = str(self.hour).zfill(2)
        minute = str(self.minute).zfill(2)
        second = str(self.second).zfill(2)
        res = f'{hour}:{minute}:{second}'
        if self.millisecond > 0:
            res += '.' + str(self.millisecond).zfill(3)
        if self.tzMinuteOffset == 0:
            res += 'Z'
        else:
            tzHour = self.tzMinuteOffset // 60
            tzMin = self.tzMinuteOffset % 60
            res += '-' if self.tzMinuteOffset < 0 else '+'
            res += str(abs(tzHour)).zfill(2) + ':'
            res += str(abs(tzMin)).zfill(2)
        return res