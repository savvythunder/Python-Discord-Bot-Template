"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.3.0
"""

import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_warn(
        self, user_id: int, server_id: int, moderator_id: int, reason: str
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    reason,
                ),
            )
            await self.connection.commit()
            return warn_id

    async def remove_warn(self, warn_id: int, user_id: int, server_id: int) -> int:
        """
        This function will remove a warn from the database.

        :param warn_id: The ID of the warn.
        :param user_id: The ID of the user that was warned.
        :param server_id: The ID of the server where the user has been warned
        """
        await self.connection.execute(
            "DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?",
            (
                warn_id,
                user_id,
                server_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    async def get_warnings(self, user_id: int, server_id: int) -> list:
        """
        This function will get all the warnings of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the warnings of the user.
        """
        rows = await self.connection.execute(
            "SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list
    async def is_command_enabled(self, server_id: int, command: str) -> bool:
        """
        This function checks if a command is enabled for a server.

        :param server_id: The ID of the server.
        :param command: The command to check.
        :return: True if the command is enabled, False otherwise.
        """
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM disabled_commands WHERE server_id=? AND command=?",
            (server_id, command),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] == 0 if result else True
    async def is_command_disabled(self, server_id: int, command: str) -> bool:
        """
        This function checks if a command is disabled for a server.

        :param server_id: The ID of the server.
        :param command: The command to check.
        :return: True if the command is disabled, False otherwise.
        """
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM disabled_commands WHERE server_id=? AND command=?",
            (server_id, command),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] > 0 if result else False
    async def disable_command(self, server_id: int, command: str) -> None:
        """
        This function disables a command for a server.

        :param server_id: The ID of the server.
        :param command: The command to disable.
        """
        await self.connection.execute(
            "INSERT OR IGNORE INTO disabled_commands(server_id, command) VALUES (?, ?)",
            (server_id, command),
        )
        await self.connection.commit()
    async def enable_command(self, server_id: int, command: str) -> None:
        """
        This function enables a command for a server.

        :param server_id: The ID of the server.
        :param command: The command to enable.
        """
        await self.connection.execute(
            "DELETE FROM disabled_commands WHERE server_id=? AND command=?",
            (server_id, command),
        )
        await self.connection.commit()
    async def get_disabled_commands(self, server_id: int) -> list:
        """
        This function gets all the disabled commands for a server.

        :param server_id: The ID of the server.
        :return: A list of all the disabled commands for the server.
        """
        rows = await self.connection.execute(
            "SELECT command FROM disabled_commands WHERE server_id=?",
            (server_id,),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            return [row[0] for row in result] if result else []
    async def is_cog_enabled(self, server_id: int, cog: str) -> bool:
        """
        This function checks if a cog is enabled for a server.

        :param server_id: The ID of the server.
        :param cog: The cog to check.
        :return: True if the cog is enabled, False otherwise.
        """
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM disabled_cogs WHERE server_id=? AND cog=?",
            (server_id, cog),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] == 0 if result else True
    async def is_cog_disabled(self, server_id: int, cog: str) -> bool:
        """
        This function checks if a cog is disabled for a server.

        :param server_id: The ID of the server.
        :param cog: The cog to check.
        :return: True if the cog is disabled, False otherwise.
        """
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM disabled_cogs WHERE server_id=? AND cog=?",
            (server_id, cog),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] > 0 if result else False
    async def enable_cog(self, server_id: int, cog: str) -> None:
        """
        This function enables a cog for a server.

        :param server_id: The ID of the server.
        :param cog: The cog to enable.
        """
        await self.connection.execute(
            "DELETE FROM disabled_cogs WHERE server_id=? AND cog=?",
            (server_id, cog),
        )
        await self.connection.commit()
    async def disable_cog(self, server_id: int, cog: str) -> None:
        """
        This function disables a cog for a server.

        :param server_id: The ID of the server.
        :param cog: The cog to disable.
        """
        await self.connection.execute(
            "INSERT OR IGNORE INTO disabled_cogs(server_id, cog) VALUES (?, ?)",
            (server_id, cog),
        )
        await self.connection.commit()
    async def get_disabled_cogs(self, server_id: int) -> list:
        """
        This function gets all the disabled cogs for a server.

        :param server_id: The ID of the server.
        :return: A list of all the disabled cogs for the server.
        """
        rows = await self.connection.execute(
            "SELECT cog FROM disabled_cogs WHERE server_id=?",
            (server_id,),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            return [row[0] for row in result] if result else []
    async def set_prefix(self, server_id: int, prefix: str) -> None:
        """
        This function sets the prefix for a server.

        :param server_id: The ID of the server.
        :param prefix: The prefix to set.
        """
        await self.connection.execute(
            "INSERT OR REPLACE INTO prefixes(server_id, prefix) VALUES (?, ?)",
            (server_id, prefix),
        )
        await self.connection.commit()

    async def get_prefix(self, server_id: int) -> str:
        """
        This function gets the prefix for a server.

        :param server_id: The ID of the server.
        :return: The prefix for the server.
        """
        rows = await self.connection.execute(
            "SELECT prefix FROM prefixes WHERE server_id=?",
            (server_id,),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None