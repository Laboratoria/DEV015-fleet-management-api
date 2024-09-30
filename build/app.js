"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
//aqui se desarrolla la api
const express_1 = __importDefault(require("express"));
const client_1 = require("@prisma/client"); //importa prisma para interactuar con BBDD
const app = (0, express_1.default)();
const prisma = new client_1.PrismaClient();
const PORT = 3001;
app.use(express_1.default.json()); // para que el servidor entienda las solicitudes de datos en formato JSON
app.use('/', (req, res) => {
    res.send('Hello world!');
});
// se crea la consulta para obtener los patentes de la tabla de la bbdd
app.use('/taxis/plate', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const taxis = yield prisma.taxis.findMany({
            select: {
                plate: true,
            },
        });
        res.json(taxis);
    }
    catch (error) {
        res.status(500).json({ error: 'Error al obtener los registros' });
    }
}));
app.listen(PORT, () => {
    console.log('SERVER IS UP ON PORT:', PORT);
});
