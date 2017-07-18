from collections import deque
import asyncio
# tuto https://zestedesavoir.com/articles/1568/decouvrons-la-programmation-asynchrone-en-python/

STATUS_NEW = 'NEW'
STATUS_RUNNING = 'RUNNING'
STATUS_FINISHED = 'FINISHED'
STATUS_ERROR = 'ERROR'
STATUS_CANCELLED = "CANCELLED"

def tic_tac():
    print("Tic")
    yield
    print("Tac")
    yield
    return ("Boum!")

def spam():
    print("Spam")
    yield
    print("Eggs")
    yield
    print("Bacon")
    yield
    return("SPAM!")

def example():
    print("Tâche 'example'")
    print("Lancement de la tâche 'subtask'")
    yield from subtask()
    print("Retour dans 'example'")
    for _ in range(3):
        print("(example)")
        yield

def example2():
    print("Tâche 'example'")
    print("Lancement de la tâche 'subtask'")
    ensure_future(subtask())   # <- appel à ensure_future au lieu de yield from
    print("Retour dans 'example'")
    for _ in range(3):
        print("(example)")
        yield

def subtask():
    print("Tâche 'subtask'")
    for _ in range(2):
        print("(subtask)")
        yield

def ensure_future(coro, loop=None):
    if loop is None:
        loop = Loop()
    return loop.schedule(coro)

def cancel(task):
    # On annule la tâche
    task.cancel()
    # On laisse la main à la boucle événementielle pour qu'elle ait l'occasion
    # de prendre en compte l'annulation
    yield


class Task:
    def __init__(self, coro):
        self.coro = coro  # Coroutine à exécuter
        self.name = coro.__name__
        self.status = STATUS_NEW  # Statut de la tâche
        self.return_value = None  # Valeur de retour de la coroutine
        self.error_value = None  # Exception levée par la coroutine

    # Exécute la tâche jusqu'à la prochaine pause
    def run(self):
        try:
            # On passe la tâche à l'état RUNNING et on l'exécute jusqu'à
            # la prochaine suspension de la coroutine.
            self.status = STATUS_RUNNING
            next(self.coro)
        except StopIteration as err:
            # Si la coroutine se termine, la tâche passe à l'état FINISHED
            # et on récupère sa valeur de retour.
            self.status = STATUS_FINISHED
            self.return_value = err.value
        except Exception as err:
            # Si une autre exception est levée durant l'exécution de la
            # coroutine, la tâche passe à l'état ERROR, et on récupère
            # l'exception pour laisser l'utilisateur la traiter.
            self.status = STATUS_ERROR
            self.error_value = err

    def is_done(self):
        return self.status in {STATUS_FINISHED, STATUS_ERROR}

    def cancel(self):
        if self.is_done():
            # Inutile d'annuler une tâche déjà terminée
            return
        self.status = STATUS_CANCELLED

    def is_cancelled(self):
        return self.status == STATUS_CANCELLED

    def __repr__(self):
        result = ''
        if self.is_done():
            result = " ({!r})".format(self.return_value or self.error_value)

        return "<Task '{}' [{}]{}>".format(self.name, self.status, result)

class Loop:
    def __init__(self):
        self._running = deque()

    def _loop(self):
        task = self._running.popleft()
        task.run()
        if task.is_done():
            print(task)
            return
        if task.is_cancelled():
            # Si la tâche a été annulée,
            # on ne l'exécute pas et on "l'oublie".
            print(task)
            return
        self.schedule(task)


    def run_until_empty(self):
        while self._running:
            self._loop()

    def schedule(self, task):
        if not isinstance(task, Task):
            task = Task(task)
        self._running.append(task)
        return task

    def run_until_complete(self, task):
        task = self.schedule(task)
        while not task.is_done():
            self._loop()

def  manual_execution():
    task = tic_tac()
    next(task) # --> Tic
    next(task) # --> Tac
    next(task) # --> Boom


def one_instance():
    task = Task(tic_tac())
    while not task.is_done():
        task.run()
        print(task)
    print(task.return_value)

def two_instances():
    running_tasks = deque()
    running_tasks.append(Task(tic_tac()))
    running_tasks.append(Task(tic_tac()))
    while running_tasks:
        # On récupère une tâche en attente et on l'exécute
        task = running_tasks.popleft()
        task.run()
        if task.is_done():
        # Si la tâche est terminée, on l'affiche
             print(task)
        else:
            # La tâche n'est pas finie, on la replace au bout
            # de la file d'attente
            running_tasks.append(task)

def execution_with_loop():
    event_loop = Loop()
    event_loop.schedule(tic_tac())
    event_loop.schedule(spam())
    event_loop.run_until_empty()
    event_loop = Loop()
    event_loop.run_until_complete(tic_tac())

def execution_with_async():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tic_tac())
    loop.run_until_complete(asyncio.wait([tic_tac(), spam()]))

def sequentiel_access():
    # lancer une tache sequentielle a l interieur d une coroutine
    event_loop = Loop()
    event_loop.run_until_complete(example())

def concurrent_task():
    event_loop = Loop()
    event_loop.run_until_complete(example2())

def avec_annulation():
    print("Tâche 'example'")
    print("Lancement de la tâche 'subtask'")
    sub = ensure_future(subtask())
    print("Retour dans 'example'")
    for _ in range(3):
        print("(example)")
        yield
    yield from cancel(sub)

if __name__ == "__main__":
    #manual_execution()
    #one_instance()
    #two_instances()
    #execution_with_loop()
    #execution_with_async()
    #sequentiel_access()
    #concurrent_task()
    avec_annulation()