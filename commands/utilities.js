const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

/* 
   UTILITÁRIOS GERAIS
   Aqui tem Ping, Help, Perfil e Avatar.
   Tudo num arquivo só pra não poluir.
*/

const pingCommand = {
    data: new SlashCommandBuilder()
        .setName('ping')
        .setDescription('Responde com Pong e a latência.'),
    async execute(interaction) {
        const sent = await interaction.reply({ content: 'Pingando...', fetchReply: true });
        interaction.editReply(`🏓 Pong! 
Latência: ${sent.createdTimestamp - interaction.createdTimestamp}ms`);
    },
};

const helpCommand = {
    data: new SlashCommandBuilder()
        .setName('help')
        .setDescription('Mostra o manual de sobrevivência do servidor.'),
    async execute(interaction) {
        const commands = interaction.client.commands;
        
        const embed = new EmbedBuilder()
            .setColor(0x5865F2)
            .setTitle('📜 Ajuda do Alberto')
            .setDescription('Eu não sou pago pra isso, mas aqui estão meus comandos:')
            .setTimestamp();

        commands.forEach(cmd => {
            embed.addFields({ 
                name: `/${cmd.data.name}`, 
                value: cmd.data.description || 'Sem descrição', 
                inline: true 
            });
        });

        await interaction.reply({ embeds: [embed] });
    },
};

const perfilCommand = {
    data: new SlashCommandBuilder()
        .setName('perfil')
        .setDescription('Xereta a vida de alguém (stalker).')
        .addUserOption(option => 
            option.setName('user').setDescription('Quem você quer investigar?')),
    async execute(interaction) {
        const target = interaction.options.getMember('user') || interaction.member;
        
        const embed = new EmbedBuilder()
            .setColor(target.displayHexColor)
            .setThumbnail(target.user.displayAvatarURL({ dynamic: true }))
            .setTitle(`🕵️ Dossiê de ${target.displayName}`)
            .addFields(
                { name: '🆔 ID', value: target.id, inline: true },
                { name: '📅 Criou a conta em', value: target.user.createdAt.toLocaleDateString('pt-BR'), inline: true },
                { name: '🚀 Entrou no server em', value: target.joinedAt.toLocaleDateString('pt-BR'), inline: true },
                { name: '🎭 Cargos', value: target.roles.cache.map(r => r).join(' ').replace('@everyone', '') || 'Nenhum' }
            )
            .setFooter({ text: 'Se fosse a polícia eu já tinha achado.' });

        await interaction.reply({ embeds: [embed] });
    },
};

const avatarCommand = {
    data: new SlashCommandBuilder()
        .setName('avatar')
        .setDescription('Rouba a foto de perfil de alguém em 4K.')
        .addUserOption(option => 
            option.setName('user').setDescription('De quem é a foto?')),
    async execute(interaction) {
        const user = interaction.options.getUser('user') || interaction.user;
        const avatarUrl = user.displayAvatarURL({ dynamic: true, size: 4096 });

        const embed = new EmbedBuilder()
            .setColor(0xED4245)
            .setTitle(`📸 Avatar de ${user.username}`)
            .setImage(avatarUrl)
            .setDescription(`[Clique aqui para baixar](${avatarUrl})`);

        await interaction.reply({ embeds: [embed] });
    },
};

module.exports = [pingCommand, helpCommand, perfilCommand, avatarCommand];