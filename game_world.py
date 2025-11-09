world = [[] for _ in range(4)]
collision_pairs = {}
objects_to_remove = []

def add_object(o, depth=0):
    world[depth].append(o)


def add_objects(ol, depth=0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()


def remove_object(o):
    global objects_to_remove
    if o not in objects_to_remove:
        objects_to_remove.append(o)


def remove_objects():
    global objects_to_remove
    for o in objects_to_remove:
        for layer in world:
            if o in layer:
                layer.remove(o)
                break
    objects_to_remove.clear()


def clear():
    global world, objects_to_remove
    for layer in world:
        layer.clear()
    objects_to_remove.clear()


def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

    collision_pairs.clear()
    remove_objects()
