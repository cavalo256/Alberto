const { SlashCommandBuilder, PermissionFlagsBits, EmbedBuilder } = require('discord.js');

/*
    🔨 MODERAÇÃO PESADA
    Cuidado com esse arquivo. Aqui a gente bane, chuta e cala a boca.
    Usei PermissionFlagsBits pra garantir que só mod use isso.
*/

const banCommand = {
    data: new SlashCommandBuilder()
        .setName('ban')
        .setDescription('Aplica o martelo do banimento.')
        .addUserOption(option => 
            option.setName('user').setDescription('O meliante a ser banido').setRequired(true))
        .addStringOption(option => 
            option.setName('motivo').setDescription('Por que ele merece?'))
        .setDefaultMemberPermissions(PermissionFlagsBits.BanMembers),
    async execute(interaction) {
        const target = interaction.options.getUser('user');
        const reason = interaction.options.getString('motivo') || 'Sem motivo, só porque eu quis.';
        
        // Tenta pegar o membro no servidor
        const member = await interaction.guild.members.fetch(target.id).catch(() => null);

        if (!member) {
            return interaction.reply({ content: '❌ Esse usuário nem tá no servidor, doido.', ephemeral: true });
        }

        if (!member.bannable) {
            return interaction.reply({ content: '❌ Não consigo banir esse cara. Ele deve ser mais forte que eu (cargo maior).', ephemeral: true });
        }

        // Tenta mandar DM antes de banir
        await target.send(`🔨 Você foi banido de **${interaction.guild.name}**.
📝 Motivo: ${reason}`).catch(() => {});

        await member.ban({ reason: reason });

        const embed = new EmbedBuilder()
            .setColor(0xFF0000)
            .setTitle('🔨 BAN HAMMER')
            .setDescription(`**${target.tag}** foi jogar no Vasco.`)
            .addFields(
                { name: '👮 Mod', value: interaction.user.tag, inline: true },
                { name: '📝 Motivo', value: reason, inline: true }
            )
            .setTimestamp();

        await interaction.reply({ embeds: [embed] });
    },
};

const kickCommand = {
    data: new SlashCommandBuilder()
        .setName('kick')
        .setDescription('Expulsa (mas ele pode voltar com convite).')
        .addUserOption(option => 
            option.setName('user').setDescription('O alvo').setRequired(true))
        .addStringOption(option => 
            option.setName('motivo').setDescription('Motivo'))
        .setDefaultMemberPermissions(PermissionFlagsBits.KickMembers),
    async execute(interaction) {
        const target = interaction.options.getMember('user');
        const reason = interaction.options.getString('motivo') || 'Tchau obrigado.';

        if (!target) return interaction.reply({ content: '❌ Usuário não encontrado.', ephemeral: true });
        if (!target.kickable) return interaction.reply({ content: '❌ Não posso chutar alguém com cargo maior que o meu.', ephemeral: true });

        await target.send(`🦶 Você foi expulso de **${interaction.guild.name}**.
📝 Motivo: ${reason}`).catch(() => {});
        await target.kick(reason);

        await interaction.reply(`🦶 **${target.user.tag}** foi convidado a se retirar por **${interaction.user.tag}**.`);
    },
};

const muteCommand = {
    data: new SlashCommandBuilder()
        .setName('mute')
        .setDescription('Deixa o usuário de castigo (Timeout).')
        .addUserOption(option => 
            option.setName('user').setDescription('O tagarela').setRequired(true))
        .addIntegerOption(option => 
            option.setName('tempo').setDescription('Minutos de silêncio').setRequired(true))
        .addStringOption(option => 
            option.setName('motivo').setDescription('Motivo'))
        .setDefaultMemberPermissions(PermissionFlagsBits.ModerateMembers),
    async execute(interaction) {
        const target = interaction.options.getMember('user');
        const minutes = interaction.options.getInteger('tempo');
        const reason = interaction.options.getString('motivo') || 'Shhh 🤫';

        if (!target) return interaction.reply({ content: '❌ Usuário não encontrado.', ephemeral: true });
        if (!target.moderatable) return interaction.reply({ content: '❌ Não posso mutar esse admin.', ephemeral: true });

        // Aplica o Timeout (Mute moderno do Discord)
        await target.timeout(minutes * 60 * 1000, reason);

        const embed = new EmbedBuilder()
            .setColor(0xFFA500)
            .setDescription(`🔇 **${target.user.tag}** tomou mute de **${minutes} minutos**.
📝 Motivo: ${reason}`);

        await interaction.reply({ embeds: [embed] });
    },
};

const limparCommand = {
    data: new SlashCommandBuilder()
        .setName('limpar')
        .setDescription('Faxina no chat.')
        .addIntegerOption(option => 
            option.setName('quantidade')
            .setDescription('Quantas mensagens apagar (1-100)')
            .setMinValue(1)
            .setMaxValue(100)
            .setRequired(true))
        .addUserOption(option => 
            option.setName('user').setDescription('Apagar só desse usuário (Opcional)'))
        .setDefaultMemberPermissions(PermissionFlagsBits.ManageMessages),
    async execute(interaction) {
        const amount = interaction.options.getInteger('quantidade');
        const target = interaction.options.getUser('user');

        await interaction.deferReply({ ephemeral: true }); // Responde só pro mod, pra não poluir

        const channel = interaction.channel;
        const messages = await channel.messages.fetch({ limit: amount });

        let messagesToDelete = messages;

        // Se especificou usuário, filtra
        if (target) {
            messagesToDelete = messages.filter(m => m.author.id === target.id);
        }

        if (messagesToDelete.size === 0) {
            return interaction.editReply('❌ Nenhuma mensagem encontrada pra apagar com esses filtros.');
        }

        await channel.bulkDelete(messagesToDelete, true).catch(err => {
            return interaction.editReply('❌ Deu erro. Mensagens com mais de 14 dias não podem ser apagadas em massa.');
        });

        const feedback = target 
            ? `🧹 Apaguei **${messagesToDelete.size}** mensagens de **${target.tag}**.`
            : `🧹 Faxina completa! **${messagesToDelete.size}** mensagens foram pro lixo.`;

        await interaction.editReply(feedback);
    },
};

module.exports = [banCommand, kickCommand, muteCommand, limparCommand];