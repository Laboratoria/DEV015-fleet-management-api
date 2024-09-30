//aqui se desarrolla la api y se escribe el codigo 
import express, { Application, Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';  //importa prisma para interactuar con BBDD

const app: Application = express();

const prisma = new PrismaClient();

const PORT: number = 3001;

app.use(express.json());  // para que el servidor entienda las solicitudes de datos en formato JSON

app.use('/', async(req: Request, res: Response): Promise<void> => {
    const taxis = await prisma.taxis.findMany()
    res.json(taxis);
});

/*se crea la consulta para obtener los patentes de la tabla de la bbdd
app.get('/taxis/plate', async (req: Request, res: Response): Promise<void> => {
    try {
        const taxis = await prisma.taxis.findMany({
            select:{
                plate: true,
            },
        });
        res.json(taxis);
    } catch (error) {
        res.status(500).json({ error: 'Error al obtener los registros' });
    }
});*/



app.listen(PORT, (): void => { // esto inica el servidor siempre al ultimo
    console.log('SERVER IS UP ON PORT:', PORT);
});