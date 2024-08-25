import yaml
import random
import os

townsfolk = ["洗衣妇", "图书管理员", "调查员", "厨师", "共情者", "占卜师", "送葬者", "僧侣", "守鸦人", "处女", "杀手", "士兵", "市长"]
outsiders = ["管家", "酒鬼", "隐士", "圣徒"]
minions = ["投毒者", "猩红女郎", "间谍", "男爵"]
demons = ["小恶魔"]

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

# 清除屏幕 (用于隐藏角色信息)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# 分配角色
def assign_roles(config):
    player_ids = config['players_ids']
    forced_roles = config.get('forced_roles', [])
    excluded_roles = config.get('excluded_roles', [])
    random_roles = config.get('random_roles', {})

    roles_distribution = {
        'townsfolk': townsfolk.copy(),
        'outsiders': outsiders.copy(),
        'minions': minions.copy(),
        'demons': demons.copy()
    }
    for role_type, role_list in roles_distribution.items():
        roles_distribution[role_type] = [role for role in role_list if role not in excluded_roles]

    assigned_roles = []
    available_player_ids = set(player_ids)
    player_ids_preset = []
    seats_preset = []
    
    available_seats = list(range(1, len(player_ids) + 1))

    # 强制分配的角色
    townsfolk_count, outsider_count, minion_count, demon_count = get_role_counts(len(player_ids))
    for role_entry in forced_roles:
        player_id = role_entry.get('player_id', None)
        if player_id:
            available_player_ids.remove(player_id)
        seat = role_entry.get('seat', None)
        if seat:
            available_seats.remove(seat)
    
    if '酒鬼' in random_roles:
        drunk_role = random_roles['酒鬼']
        player_id = drunk_role.get('player_id', None)
        seat = drunk_role.get('seat', None)
        if player_id:
            available_player_ids.remove(player_id)
        if seat:
            available_seats.remove(seat)


    for role_entry in forced_roles:
       if available_player_ids:
            player_id = role_entry.get('player_id', None)
    
            if not player_id:
                player_id = available_player_ids.pop()
            seat = role_entry.get('seat', None)
            if not seat:
                seat = available_seats.pop(random.randint(0, len(available_seats) - 1))
            assigned_roles.append({
                'player_id': player_id,
                'seat': seat,
                'role': role_entry['role'],
                'alignment': get_alignment(role_entry['role'])
            })
            if role_entry['role'] in townsfolk:
               townsfolk_count -= 1
            elif role_entry['role'] in outsiders:
               outsider_count -= 1
            elif role_entry['role'] in minions:
               minion_count -= 1
               if role_entry['role'] == '男爵':
                  outsider_count += 2
                  townsfolk_count -=2
            remove_role_from_distribution(role_entry['role'], roles_distribution)

    # 分配酒鬼
    drunk_fake_role = None
    if '酒鬼' in random_roles and available_player_ids:
        drunk_role = random_roles['酒鬼']
        fake_role_options = [role for role in roles_distribution['townsfolk'] if role not in excluded_roles]
        drunk_fake_role = drunk_role.get('fake_role', random.choice(fake_role_options))
        player_id = drunk_role.get('player_id', None)

        if not player_id:
            player_id = available_player_ids.pop()
        seat = drunk_role.get('seat', None)
        # 酒鬼座位号
        if not seat:
            seat = available_seats.pop(random.randint(0, len(available_seats) - 1))
        assigned_roles.append({
            'player_id': player_id,
            'seat': seat,
            'role': drunk_fake_role,
            'alignment': "外来者",
            'real_role': '酒鬼'
        })
        available_player_ids.discard(player_id)
        # 移除酒鬼误认为的村民角色
        if drunk_fake_role in roles_distribution['townsfolk']:
            roles_distribution['townsfolk'].remove(drunk_fake_role)
        roles_distribution['outsiders'].remove('酒鬼')
    outsider_count -= 1

    # 角色分配（确保每个玩家都分配到角色）
    assign_random_roles(townsfolk_count, outsider_count, minion_count, demon_count, roles_distribution, assigned_roles, excluded_roles, available_player_ids, available_seats)

    # 按座位号排序角色信息
    assigned_roles.sort(key=lambda x: x['seat'])

    # 按回车键展示下一个玩家
    for player in assigned_roles:
        input(f"请按回车键展示座位号 {player['seat']} 的玩家信息...")
        clear_screen()
        role_info = f"玩家ID: {player['player_id']}, 座位号: {player['seat']}, 角色: {player['role']}, 阵营: {player['alignment']}"
        print(role_info)
        input("按回车键隐藏此信息...")
        clear_screen()

    log_all_roles(assigned_roles)

    # 处理未被分配的角色和排除的角色
    handle_unassigned_and_exclusive_roles(roles_distribution, excluded_roles, get_role_counts(len(player_ids))[2] + get_role_counts(len(player_ids))[3])

# 获取角色阵营
def get_alignment(role):
    if role in townsfolk:
        return "村民"
    elif role in outsiders:
        return "外来者"
    elif role in minions:
        return "爪牙"
    elif role in demons:
        return "恶魔"

# 移除已分配的角色
def remove_role_from_distribution(role, roles_distribution):
    for role_type, roles in roles_distribution.items():
        if role in roles:
            roles.remove(role)
            break

# 确定各类角色的数量
def get_role_counts(players_count):
    if players_count == 5:
        return 3, 0, 1, 1
    elif players_count == 6:
        return 3, 1, 1, 1
    elif players_count == 7:
        return 5, 0, 1, 1
    elif players_count == 8:
        return 5, 1, 1, 1
    elif players_count == 9:
        return 5, 2, 1, 1
    elif players_count == 10:
        return 7, 0, 2, 1
    elif players_count == 11:
        return 7, 1, 2, 1 
    elif players_count == 12:
        return 7, 2, 3, 1
    elif players_count == 13:
        return 9, 0, 3, 1
    elif players_count == 14:
        return 9, 1, 3, 1
    elif players_count == 15:
        return 9, 2, 3, 1
    return 7, 0, 2, 1  # 默认值

# 随机分配未指定角色
def assign_random_roles(townsfolk_count, outsider_count, minion_count, demon_count, roles_distribution, assigned_roles, excluded_roles, available_player_ids, available_seats):
    print("开始随机分配角色")
    available_roles = [role for role in roles_distribution['minions'] if role not in excluded_roles]
    selected_roles = random.sample(available_roles, min(minion_count, len(available_roles)))
    for role in selected_roles:
            if role == '男爵':
                townsfolk_count -= 2
                outsider_count += 2
            if available_player_ids:  
                player_id = available_player_ids.pop()
                seat = available_seats.pop(random.randint(0, len(available_seats) - 1))
                assigned_roles.append({
                    'player_id': player_id,
                    'seat': seat,
                    'role': role,
                    'alignment': get_alignment(role)
                })
                remove_role_from_distribution(role, roles_distribution)


    for role_type, count in zip(['townsfolk', 'outsiders'], [townsfolk_count, outsider_count]):
        available_roles = [role for role in roles_distribution[role_type] if role not in excluded_roles]
        selected_roles = random.sample(available_roles, min(count, len(available_roles)))
        for role in selected_roles:
            if role == '男爵':
                townsfolk_count -= 2
                outsider_count += 2
            if available_player_ids:  
                player_id = available_player_ids.pop()
                seat = available_seats.pop(random.randint(0, len(available_seats) - 1))
                assigned_roles.append({
                    'player_id': player_id,
                    'seat': seat,
                    'role': role,
                    'alignment': get_alignment(role)
                })
                remove_role_from_distribution(role, roles_distribution)

# 打印和log所有玩家的角色信息
def log_all_roles(assigned_roles):
    print("\n所有玩家的角色信息:")
    for player in assigned_roles:
        role_info = f"玩家ID: {str(player['player_id']).ljust(12)}, 座位号: {str(player['seat']).ljust(6)}, 角色: {player['role'].ljust(8)}, 阵营: {player['alignment'].ljust(6)}"
        if player.get('real_role') == '酒鬼':
            role_info += f" (真实身份: 酒鬼, 误以为身份: {player['role']})"
        print(role_info)

# 打印和log未分配的角色以及排除的角色
def handle_unassigned_and_exclusive_roles(roles_distribution, excluded_roles, evil_player_count):
    print("\n未被分配的角色, 不包括玩家强行排除的未分配角色:")
    unassigned_roles = []
    for role_type, roles in roles_distribution.items():
        if roles:
            unassigned_roles.extend(roles)
            print(f"{role_type}: {', '.join(roles)}")

    # 如果排除的角色数量不足邪恶玩家数量，则从未分配的村民和外来者中随机排除
    remaining_exclusive_roles_needed = evil_player_count - len(excluded_roles)
    #print(remaining_exclusive_roles_needed)
    if remaining_exclusive_roles_needed > 0:
        unassigned_good_roles = roles_distribution['townsfolk'] + roles_distribution['outsiders']
        additional_exclusive_roles = random.sample(unassigned_good_roles, remaining_exclusive_roles_needed)
        excluded_roles.extend(additional_exclusive_roles)

    print("\n排除的角色:")
    # 将YAML中指定的排除角色以及随机生成的排除角色都展示出来
    print("邪恶阵营已知的排除角色:")
    #print(excluded_roles)
    for role in excluded_roles:
    	if isinstance(role, dict):
        	for value in role.values():
            		print(value, end=', ')
    	else:
        	print(role, end=', ')
# 主程序
if __name__ == "__main__":
    config_file = 'game_script.yaml'
    config = load_config(config_file)
    assign_roles(config)

