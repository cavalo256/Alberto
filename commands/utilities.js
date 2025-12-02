const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

/* 
   Aqui tá a mágica que você pediu:
   Dois comandos num arquivo só. O dev chora, mas o cliente sorri.
*/

const pingCommand = {
    data: new SlashCommandBuilder()
        .setName('ping')
        .setDescription('Responde com Pong e a latência (se o wi-fi ajudar).'),
    async execute(interaction) {
        const sent = await interaction.reply({ content: 'Pingando...', fetchReply: true });
        interaction.editReply(`🏓 Pong! 
Latência: ${sent.createdTimestamp - interaction.createdTimestamp}ms`);
    },
};

const helpCommand = {
    data: new SlashCommandBuilder()
        .setName('help')
        .setDescription('Mostra tudo que o Alberto sabe fazer.'),
    async execute(interaction) {
        const commands = interaction.client.commands;
        
        const embed = new EmbedBuilder()
            .setColor(0x5865F2)
            .setTitle('📜 Ajuda do Alberto')
            .setDescription('Eu sou o Alberto. Segue o menu:')
            .setTimestamp();

        commands.forEach(cmd => {
            embed.addFields({ 
                name: `/${cmd.data.name}`, 
                value: cmd.data.description || 'Sem descrição', 
                inline: false 
            });
        });

        await interaction.reply({ embeds: [embed] });
    },
};

// Exportando como array pra gente varrer lá no index.js
module.exports = [pingCommand, helpCommand];