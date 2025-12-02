const { SlashCommandBuilder } = require('discord.js');

/*
    COMANDOS DE DIVERSÃO
    Dados, moedas e aleatoriedades.
*/

const moedaCommand = {
    data: new SlashCommandBuilder()
        .setName('moeda')
        .setDescription('Cara ou Coroa pra decidir quem lava a louça.'),
    async execute(interaction) {
        // Suspense fake
        await interaction.reply('🪙 Girando a moeda...');
        
        setTimeout(async () => {
            const result = Math.random() > 0.5 ? '👑 Coroa' : '🗿 Cara';
            await interaction.editReply(`Caiu: **${result}**!`);
        }, 1500);
    },
};

const dadoCommand = {
    data: new SlashCommandBuilder()
        .setName('dado')
        .setDescription('Rola dados (D6, D20, D100, você escolhe).')
        .addIntegerOption(option => 
            option.setName('lados')
            .setDescription('Quantos lados? (Padrão: 6)')
            .setMinValue(2))
        .addIntegerOption(option => 
            option.setName('quantidade')
            .setDescription('Quantos dados? (Padrão: 1)')
            .setMinValue(1)
            .setMaxValue(10)),
    async execute(interaction) {
        const lados = interaction.options.getInteger('lados') || 6;
        const qtd = interaction.options.getInteger('quantidade') || 1;

        let results = [];
        let sum = 0;

        for (let i = 0; i < qtd; i++) {
            const val = Math.floor(Math.random() * lados) + 1;
            results.push(val);
            sum += val;
        }

        const msg = qtd > 1 
            ? `🎲 **Resultados:** [${results.join(', ')}]
🔢 **Total:** ${sum}`
            : `🎲 O dado de ${lados} lados caiu em: **${results[0]}**`;

        await interaction.reply(msg);
    },
};

module.exports = [moedaCommand, dadoCommand];