import asyncio
from datetime import datetime
SODA_LOCK = asyncio.Lock()
BURGER_SEM = asyncio.Semaphore(3)
FRIES_COUNTER = 0
FRIES_LOCK = asyncio.Lock()

async def get_soda(client):
    # Acquisition du verrou
    # la syntaxe 'async with FOO' peut être lue comme 'with (yield from FOO)'
    async with SODA_LOCK:
        # Une seule tâche à la fois peut exécuter ce bloc
        print("    > Remplissage du soda pour {}".format(client))
        await asyncio.sleep(1)
        print("    < Le soda de {} est prêt".format(client))

async def get_fries(client):
    global FRIES_COUNTER
    async with FRIES_LOCK:
        print("    > Récupération des frites pour {}".format(client))
        if FRIES_COUNTER == 0:
            print("   ** Démarrage de la cuisson des frites")
            await asyncio.sleep(4)
            FRIES_COUNTER = 5
            print("   ** Les frites sont cuites")
        FRIES_COUNTER -= 1
        print("    < Les frites de {} sont prêtes".format(client))

async def get_burger(client):
    print("    > Commande du burger en cuisine pour {}".format(client))
    async with BURGER_SEM:
        await asyncio.sleep(3)
        print("    < Le burger de {} est prêt".format(client))

async def serve(client):
    print("=> Commande passée par {}".format(client))
    start_time = datetime.now()
    await asyncio.wait(
        [
            get_soda(client),
            get_fries(client),
            get_burger(client)
        ]
    )
    total = datetime.now() - start_time
    print("<= {} servi en {}".format(client, datetime.now() - start_time))
    return total

async def perf_test(nb_requests, period, timeout):
    tasks = []
    # On lance 'nb_requests' commandes à 'period' secondes d'intervalle
    for idx in range(1, nb_requests + 1):
        client_name = "client_{}".format(idx)
        tsk = asyncio.ensure_future(serve(client_name))
        tasks.append(tsk)
        await asyncio.sleep(period)

    finished, _ = await asyncio.wait(tasks)
    success = set()
    for tsk in finished:
        if tsk.result().seconds < timeout:
            success.add(tsk)

    print("{}/{} clients satisfaits".format(len(success), len(finished)))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print ('BEFORE')
    loop.run_until_complete(asyncio.wait([serve(clt) for clt in 'ABCDEFGHIJ']))
    print('AFTER')
    #loop.run_until_complete(perf_test(10, 1, 5))