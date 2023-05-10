import random


def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == '?invite':
        return "https://discord.com/invite/GtBkk3hCD7\n" + "https://www.roblox.com/groups/5887801/The-44th#!/about"

    if p_message == '?cr':
        return 'https://www.roblox.com/games/4878805436/RAID-Calypsos-Rest'

    if p_message == '?balls':
        return 'https://www.roblox.com/games/5024119817/Dead-Mans-Maw'

    if p_message == '?olisar':
        return 'https://www.roblox.com/games/4863932809/Olisar-Briefing-Room'

    if p_message == '44 x sg':
        return 'https://cdn.discordapp.com/attachments/532361338404732929/1101375291756130365/44th_x_SG_GOAT.png'

    if p_message == 'rule 1':
        return 'Rule 1 states: Do unto others as you would have them do unto you.'

    if p_message == 'keb':
        return 'Keb\'s Law States: No man ever steps in the same river twice, for it\'s not the same river and he\'s not the same man.'

    if p_message == 'russel':
        return 'https://cdn.discordapp.com/attachments/718810904745213972/893601573069029376/Message_for_Xeqto.mp4'