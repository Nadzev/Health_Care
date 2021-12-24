import aiohttp



class Crm:
    # def __init__(self, crm, name, cpf):
    #     self.crm = crm
    #     self.name = name
    #     self.cpf = cpf

    @classmethod
    async def consulting_crm(self, crm, name):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.consultacrm.com.br/api/index.php?tipo=crm&q={name}&chave=5181281254&destino=json') as response:
                response = await response.text()
                return response

