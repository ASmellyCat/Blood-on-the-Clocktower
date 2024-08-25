# Blood on the Clocktower Automated Role Assignment / 血染钟楼自动角色分配

This project automates the role assignment process for the board game "Blood on the Clocktower." Roles are distributed based on a YAML configuration file that can specify forced roles, excluded roles, and special roles like the Drunk. The program ensures each player sees their assigned role individually, clears the screen afterward, and allows the storyteller to review all role assignments, unassigned roles, and exclusive roles shown to the evil team.

该项目自动分配桌游“血染钟楼”的游戏角色。角色分配基于YAML配置文件，该文件可指定强制角色、排除角色和特殊角色（如酒鬼）。该程序确保每位玩家单独查看其分配的角色，并在查看后清除屏幕，最后允许上帝查看所有角色分配情况、未分配角色和展示给邪恶阵营的排除角色。

## Features / 功能

- **Dynamic Role Assignment / 动态角色分配**: Automatically assigns roles based on the number of players and game rules. 根据玩家数量和游戏规则自动分配角色。
- **Individual Role Display / 角色单独展示**: Each player can individually view their assigned role, and the screen is cleared after viewing. 每个玩家可单独查看其分配的角色，查看后屏幕将被清除。
- **Drunk Mechanic / 酒鬼机制**: Supports assigning a fake role to the Drunk player, while retaining their true identity for the storyteller. 支持为酒鬼玩家分配一个虚假的村民角色，上帝可以看到真实身份。
- **Unassigned and Exclusive Roles / 未分配与排除角色**: The storyteller can review unassigned roles and roles hidden from the game but shown to the evil team. 上帝可以查看未分配的角色和展示给邪恶阵营的排除角色。

## How It Works / 工作原理

The program reads a YAML configuration file that specifies the number of players, forced roles, excluded roles, and special role settings (e.g., Drunk). Based on the number of players, the program calculates the appropriate number of Townsfolk, Outsiders, Minions, and Demons, and assigns roles accordingly.

程序读取YAML配置文件，该文件指定玩家数量、强制角色、排除角色和特殊角色设定（如酒鬼）。根据玩家数量，程序计算适当数量的村民、外来者、爪牙和恶魔角色，并相应地分配角色。

The storyteller (game master) manages the game by bringing each player to the computer to reveal their role. The program hides role details until each player is ready to view them.

上帝通过程序管理游戏，并将每个玩家带到电脑前揭示其角色。程序在每个玩家准备查看之前会隐藏角色信息。

At the end, the storyteller can view a complete list of all player roles, the unassigned roles, and the exclusive roles shown to the evil team.

在游戏结束时，上帝可以查看所有玩家的角色分配信息、未分配角色及展示给邪恶阵营的排除角色。

## Usage / 使用说明

1. **Step 1: Prepare the YAML Configuration / 步骤 1: 准备YAML配置**

   Create a YAML configuration file (e.g., `game_script.yaml`) based on your game needs. The configuration should define the number of players, the player IDs, any forced roles, excluded roles, and special roles like the Drunk.

   根据游戏需求创建YAML配置文件（例如，`game_script.yaml`）。配置文件应定义玩家数量、玩家ID、任何强制角色、排除角色以及像酒鬼这样的特殊角色。

   Example YAML configuration / YAML配置示例:

   ```yaml
   players_count: 10
   players_ids:
     - "a"
     - "b"
     - "c"
     - "d"
     - "e"
     - "f"
     - "g"
     - "h"
     - "i"
     - "j"

   forced_roles:
     - role: 小恶魔
     - role: 占卜师
       player_id: a
       seat: 1
     - role: 图书管理员
       player_id: b

   excluded_roles:
      - 洗衣妇
      - 处女

   random_roles: 
     酒鬼:
       fake_role: 厨师
       player_id: c
       seat: 5

2. **Step 2: Install the Required Libraries / 步骤 2: 安装所需库**

   Ensure that you have Python 3.x installed on your machine. You will need to install the `PyYAML` library to enable the script to parse the YAML configuration files.

   请确保已在你的机器上安装了 Python 3.x。你需要安装 `PyYAML` 库以便脚本能够解析 YAML 配置文件。

   To install `PyYAML`, run the following command in your terminal or command prompt:

   要安装 `PyYAML`，请在终端或命令提示符中运行以下命令:

   ```bash
   pip install pyyaml

3. **Step 3: Run the Python Script / 步骤 3: 运行Python脚本**

   After preparing your YAML configuration file and installing the required libraries, you are ready to run the Python script to assign roles.

   在准备好你的YAML配置文件并安装所需库后，你可以运行Python脚本来分配角色。

   To run the script, use the following command:

   运行脚本时，使用以下命令:

   ```bash
   python assign_roles.py

4. **Step 4: Follow On-Screen Prompts / 步骤 4: 按照屏幕提示操作**

   Once the script is running, the program will guide you through the process of revealing each player's role individually. Each player will approach the computer to view their role.

   一旦脚本运行，程序会引导你逐步揭示每个玩家的角色。每个玩家会依次走到电脑前查看他们的角色。

   - **Display Roles / 展示角色**: The program will prompt the storyteller to press Enter to reveal a player's role. After viewing, the screen will automatically clear to maintain secrecy.
     
     **展示角色**: 程序会提示上帝按回车键来展示玩家的角色。玩家查看后，屏幕会自动清除以保持角色的秘密。

   - **Player-Specific Prompts / 玩家特定提示**: The storyteller can bring each player to the computer one by one, and after pressing Enter, the player will see their role, seat number, alignment, and any specific abilities they may have.

     **玩家特定提示**: 上帝可以一个一个地把玩家带到电脑前，并在按下回车键后，玩家会看到自己的角色、座位号、阵营及其特定技能。

   - **Clear Screen / 清除屏幕**: After each player has viewed their role, press Enter again to clear the screen before revealing the next player's role.

     **清除屏幕**: 每个玩家查看完角色后，再次按下回车键清除屏幕，然后展示下一个玩家的角色。

   **Example**: The following message will appear for each player based on their assigned role:
   
   **示例**: 每个玩家将根据其分配的角色看到以下信息:

   ```plaintext
   玩家ID: a, 座位号: 1, 角色: 占卜师, 阵营: 村民
   玩家ID: b, 座位号: 2, 角色: 猩红女郎, 阵营: 爪牙
   玩家ID: c, 座位号: 5, 角色: 厨师 (真实身份: 酒鬼), 阵营: 外来者


5. **Step 5: Review All Roles and Exclusive Roles / 步骤 5: 审查所有角色和排除角色**

   After all players have viewed their roles, the storyteller will be presented with a summary of all the role assignments. This includes the following:

   当所有玩家都查看完他们的角色后，上帝会看到角色分配的总结信息。该信息包括以下内容:

   - **Assigned Roles / 分配的角色**: A complete list of all players, their seat numbers, assigned roles, and alignments. This allows the storyteller to keep track of the game.
     
     **分配的角色**: 显示所有玩家的完整列表，包括他们的座位号、分配的角色和阵营。这帮助上帝跟踪游戏进展。

   - **Unassigned Roles / 未分配的角色**: A list of roles that were not assigned to any player. These roles can be used by the evil team for bluffing during the game.
     
     **未分配的角色**: 显示未分配给任何玩家的角色列表。这些角色可以在游戏过程中被邪恶阵营用于伪装。

   - **Exclusive Roles / 排除的角色**: A list of roles that were excluded from the game and are known to the evil team. These roles are not in play but can be used to mislead the good team.
     
     **排除的角色**: 显示从游戏中排除且邪恶阵营已知的角色列表。这些角色未参与游戏，但可用于误导好人阵营。

   Example of the summary / 总结示例:

   ```plaintext
   所有玩家的角色信息:
   玩家ID: a, 座位号: 1, 角色: 占卜师, 阵营: 村民
   玩家ID: b, 座位号: 2, 角色: 猩红女郎, 阵营: 爪牙
   玩家ID: c, 座位号: 5, 角色: 厨师 (真实身份: 酒鬼), 阵营: 外来者

   未被分配的角色:
   村民: 洗衣妇, 市长
   爪牙: 投毒者

   邪恶阵营已知的排除角色:
   处女, 隐士, 市长

