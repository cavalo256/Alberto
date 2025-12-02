require('dotenv').config();
const { Client, GatewayIntentBits, Collection, Events } = require('discord.js');
const fs = require('fs');
const path = require('path');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

client.commands = new Collection();

// --- SISTEMA DE CARREGAMENTO AUTOMÁTICO ---
// Ele lê TUDO que estiver na pasta 'commands'
const commandsPath = path.join(__dirname, 'commands');

if (!fs.existsSync(commandsPath)) {
    fs.mkdirSync(commandsPath);
}

const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const filePath = path.join(commandsPath, file);
    const commandOrGroup = require(filePath);

    const registerCommand = (cmd) => {
        if ('data' in cmd && 'execute' in cmd) {
            client.commands.set(cmd.data.name, cmd);
            console.log(`[OK] Comando '/${cmd.data.name}' carregado do arquivo ${file}.`);
        } else {
            console.log(`[ERRO] O arquivo ${file} tem um comando quebrado.`);
        }
    };

    // Suporta tanto exportação única (module.exports = {...})
    // Quanto exportação múltipla (module.exports = [..., ...])
    if (Array.isArray(commandOrGroup)) {
        commandOrGroup.forEach(cmd => registerCommand(cmd));
    } else {
        registerCommand(commandOrGroup);
    }
}

client.once(Events.ClientReady, c => {
    console.log(`✅ Alberto tá on! Logado como ${c.user.tag}`);
    console.log(`📝 Total de comandos: ${client.commands.size}`);
});

client.on(Events.InteractionCreate, async interaction => {
    if (!interaction.isChatInputCommand()) return;

    const command = interaction.client.commands.get(interaction.commandName);

    if (!command) return;

    try {
        await command.execute(interaction);
    } catch (error) {
        console.error(error);
        const msg = { content: 'Deu ruim executando esse comando!', ephemeral: true };
        if (interaction.replied || interaction.deferred) await interaction.followUp(msg);
        else await interaction.reply(msg);
    }
});

client.login(process.env.DISCORD_TOKEN);