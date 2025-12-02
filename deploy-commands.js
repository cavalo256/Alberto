const { REST, Routes } = require('discord.js');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

/*
   ESSE ARQUIVO SERVE PRA REGISTRAR OS COMANDOS (/)
   Rode ele sempre que criar um comando novo:
   > node deploy-commands.js
*/

const commands = [];
// Pega o caminho da pasta commands
const commandsPath = path.join(__dirname, 'commands');

if (!fs.existsSync(commandsPath)) {
    console.error('❌ Cadê a pasta commands, meu patrão?');
    process.exit(1);
}

const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const filePath = path.join(commandsPath, file);
    const command = require(filePath);

    // Função auxiliar pra pegar o JSON do comando
    const grabJson = (cmd) => {
        if ('data' in cmd && 'execute' in cmd) {
            commands.push(cmd.data.toJSON());
        } else {
            console.log(`[AVISO] O comando em ${filePath} tá faltando 'data' ou 'execute'.`);
        }
    };

    // Lógica pra lidar com arrays (utilities.js) ou objetos (fun.js)
    if (Array.isArray(command)) {
        command.forEach(c => grabJson(c));
    } else {
        grabJson(command);
    }
}

const rest = new REST().setToken(process.env.DISCORD_TOKEN);

(async () => {
    try {
        console.log(`🔄 Começando a atualizar ${commands.length} comandos...`);

        // O método put substitui todos os comandos existentes pelos novos
        const data = await rest.put(
            Routes.applicationCommands(process.env.CLIENT_ID),
            { body: commands },
        );

        console.log(`✅ Sucesso! ${data.length} comandos registrados.`);
    } catch (error) {
        console.error('❌ Deu ruim no deploy:', error);
    }
})();