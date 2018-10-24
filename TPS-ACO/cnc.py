
class CNC:
    def __init__(self, tp1, tp):
        self.tp1 = tp1
        self.time_process = tp
        self.start_time = 0
        self.is_working = False
        self.production = 0

    def process(self, cur_time):
        self.start_time = cur_time
        self.is_working = True
        return self.time_process

    def is_available(self, cur_time):
        if self.is_working:
            if cur_time-self.start_time >= self.time_process:
                self.is_working = False
                self.production += 1
                return True
            else:
                return False
        else:
            return True

    def free(self):
        self.is_working = False

    def has_production(self):
        return self.production > 0

    def get_leaving_time(self, cur_time):
        return self.start_time + self.time_process - cur_time



