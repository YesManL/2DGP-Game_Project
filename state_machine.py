class StateMachine:
    def __init__(self, start_state, state_transitions):
        self.cur_state = start_state
        self.state_transitions = state_transitions
        self.cur_state.enter(('START', None))

    def update(self):
        self.cur_state.do()

    def handle_state_event(self, event):
        for check_event in self.state_transitions[self.cur_state].keys():
            if check_event(event):
                self.cur_state.exit(event)
                self.next_state = self.state_transitions[self.cur_state][check_event]
                self.next_state.enter(event)
                self.cur_state = self.next_state
                return

    def draw(self):
        self.cur_state.draw()
import time
frame_time = 0.0

running = None
stack = None

def change_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()

    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    global frame_time
    frame_time = 0.0
    current_time = time.time()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

        frame_time = time.time() - current_time
        current_time += frame_time
        frame_rate = 1.0 / frame_time if frame_time > 0 else 0

