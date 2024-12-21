"""VLC Remote Control."""

import re
import sys
import socket
import argparse
from typing import Optional
from pathlib import Path
from dataclasses import dataclass


class UnknownRemoteCommand(Exception):
    """Exception raised for unknown remote control commands."""

    def __init__(self, message="Unknown remote control command"):
        super().__init__(message)


class PausedPlayerError(Exception):
    """Exception raised when player is paused."""

    def __init__(self, message="Player is paused. Cannot proceed"):
        super().__init__(message)


@dataclass
class AudioDevice:
    """System audio device."""
    id: str
    name: str


# @dataclass
class CommandLineArgs(argparse.Namespace):
    """Command-line arguments for VLCRemoteControl."""
    host: str
    port: int
    command: Optional[str]
    file: Optional[Path]
    index: Optional[int]
    level: Optional[int]
    device_id: Optional[str]


class VLCRemoteControl:
    """Control VLC media player via Remote Control interface."""

    def __init__(self, host: str, port: int, timeout: float = 1) -> None:
        """Initialize VLCRemoteControl.

        Args:
            host (str): Hostname or IP address of the VLC instance.
            port (int): Port number of the VLC RC interface.
            timeout (float, optional):
                Socket connection timeout in seconds. Defaults to 1.
        """
        self._host = host
        self._port = port
        self._timeout = timeout

    _supported_commands: tuple[str] = (
        "add", "playlist", "play", "stop", "next", "prev",
        "goto", "repeat", "loop", "random", "clear", "status", "pause",
        "volume", "adev", "quit"
    )

    def _filter_response(self, data: list[str]) -> list[str]:
        """
        Split data by "\r\n", remove empty and duplicates.
        Order preserved.
        """
        result = []
        for item in data:
            result.extend(list(filter(None, item.split("\r\n"))))
        return list(dict.fromkeys(result))

    def _get_elements_between(
            self,
            elements: list[str],
            start_element: str,
            end_element: str
    ) -> list[str]:
        """Return elements between start_element and end_element.

        Args:
            elements (list[str]): List to search through.
            start_element (str): Element marking the start of range.
            end_element (str): Element marking the end of range.

        Returns:
            list[str]: List of elements or an empty list if not found.
        """
        try:
            start_index = elements.index(start_element) + 1
            end_index = elements.index(end_element)
            if start_index < end_index:
                return elements[start_index:end_index]
        except ValueError:
            pass
        return []

    def _has_true_flag(self, elements: list[str]) -> bool:
        """
        Check if any element in the list contains the substring 'true'.

        Args:
            elements (list[str]): List of strings to search through.

        Returns:
            bool:
                True if 'true' is found in any element,
                otherwise False. (case-insensitive)
        """
        for element in elements:
            if "true" in element.lower():
                return True
        return False

    def _send_command(self, command: str) -> list[str]:
        """Send a command to VLC and receive the response.

        Args:
            command (str): The VLC RC command to send.

        Raises:
            UnknownRemoteCommand: If the command is not recognized.
            ConnectionError: If there are issues connecting to VLC.
            PausedPlayerError: If the player is paused.

        Returns:
            list[str]: Filtered response data from VLC.
        """
        response_data: list[str] = []
        command_name = command.split()[0]
        if command_name not in self._supported_commands:
            raise UnknownRemoteCommand(f"Unknown command '{command_name}'")

        try:
            with socket.create_connection(
                (self._host, self._port), self._timeout
            ) as rc_socket:
                rc_socket.sendall(str(command).encode() + b"\n")
                rc_socket.shutdown(1)
                while True:
                    response = rc_socket.recv(4096).decode()
                    if not response:
                        break
                    response_data.append(response)
        except (TimeoutError, ConnectionRefusedError, socket.error) as error:
            message = f"VLC Remote Control is unavailable [{error}]"
            raise ConnectionError(message) from error

        if command_name != "pause":
            for i in response_data:
                if "Type 'pause' to continue." in i:
                    raise PausedPlayerError()
        return self._filter_response(response_data)

    def is_paused(self) -> bool:
        """Check if player is paused.

        Returns:
            bool: True if paused, False otherwise
        """
        response = self._send_command("status")
        if "Type 'pause' to continue." in response:
            return True
        return False

    def add(self, file: Path) -> None:
        """Add a file to the playlist.

        Args:
            file (Path): Path object representing the file to add.

        Raises:
            FileNotFoundError:
                If the specified file does not exist or is a directory.

        Returns:
            bool: True if the command was successful, False otherwise.
        """
        if not file.exists() or file.is_dir():
            raise FileNotFoundError(f"File '{file}' not found")
        self._send_command(f"add {file.as_uri()}")

    def playlist(self) -> list[str]:
        """Return items currently in playlist.

        Returns:
            list[str]: items currently in playlist
        """
        result: list[str] = []
        response = self._send_command("playlist")
        playlist = self._get_elements_between(
            response,
            "|- Playlist",
            "|- Media Library"
        )

        for i in playlist:
            match = re.search(r"\|\s\s-\s(.+)\s\(.*", i)
            try:
                result.append(match.group(1))
            except AttributeError:
                pass

        return result

    def play(self) -> None:
        """Play the current stream."""
        self._send_command("play")

    def stop(self) -> None:
        """Stop the current stream."""
        self._send_command("stop")

    def next(self) -> None:
        """Go to the next item in the playlist."""
        self._send_command("next")

    def prev(self) -> None:
        """Go to the previous item in the playlist."""
        self._send_command("prev")

    def goto(self, index: int) -> None:
        """Go to the specified playlist index.

        Args:
            index (int): The index to go to (starting from 1).

        Raises:
            ValueError: If the index is less than or equal to 0.

        Returns:
            bool: True if the command was successful, False otherwise.
        """
        if index <= 0:
            raise ValueError("Index must be greater than 0")
        self._send_command(f"goto {index}")

    def repeat(self) -> bool:
        """Toggle playlist item repeat."""
        response = self._send_command("repeat")
        return self._has_true_flag(response)

    def loop(self) -> bool:
        """Toggle playlist loop."""
        response = self._send_command("loop")
        return self._has_true_flag(response)

    def random(self) -> bool:
        """Toggle playlist random jumping."""
        response = self._send_command("random")
        return self._has_true_flag(response)

    def clear(self) -> None:
        """Clear the playlist."""
        self._send_command("clear")

    def status(self) -> list[str]:
        """Get the current playlist status."""
        return self._send_command("status")

    def pause(self):
        """Toggle pause."""
        self._send_command("pause")
        try:
            self._send_command("status")
            return False
        except PausedPlayerError:
            return True

    def get_volume(self) -> int:
        """Get the current audio volume.

        Returns:
            int:
                The current audio volume (0-320),
                or -1 if the volume could not be retrieved.
        """
        response = self._send_command("volume")
        for item in response:
            match = re.search(r"audio volume:\s*(\d+)", item)
            if match:
                return int(match.group(1))
        return -1

    def set_volume(self, value: int) -> None:
        """Set the audio volume.

        Args:
            value (int): Volume level (0-320).

        Raises:
            ValueError: If the volume is outside the range of 0-320.
            RuntimeError: If failed to set audio volume.
        """
        if not 0 <= value <= 320:
            raise ValueError("Value must be between 0 and 320")
        self._send_command(f"volume {value}")

    def get_adev(self) -> list[AudioDevice]:
        """Get a list of available audio devices."""
        devices: list[AudioDevice] = []
        response = self._send_command("adev")
        for item in response:
            if item[:2] == "| ":
                tmp = item[2:].split(" - ", 1)
                device = AudioDevice(tmp[0], tmp[1])
                if device.id:
                    devices.append(device)
        return devices

    def set_adev(self, device_id: str) -> None:
        """Set the active audio device."""
        self._send_command(f"adev {device_id}")

    def quit(self) -> None:
        """Quit VLC."""
        self._send_command("quit")


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Command Line Interface for VLC Remote Control",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "host", help="VLC host address (e.g., 127.0.0.1, 192.168.1.100)")
    parser.add_argument(
        "port", type=int, help="VLC Remote Control interface port")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Simple commands without arguments
    for cmd in ["play", "stop", "next", "prev", "clear", "status", "pause",
                "repeat", "loop", "random", "playlist", "quit"]:
        subparsers.add_parser(cmd, help=f"{cmd} command")

    # Add file to playlist
    add_parser = subparsers.add_parser("add", help="Add file to playlist")
    add_parser.add_argument("file", type=Path, help="File path")

    # Goto specific track
    goto_parser = subparsers.add_parser("goto", help="Go to specific track")
    goto_parser.add_argument("index", type=int,
                             help="Track index (starts at 1)")

    # Volume control
    volume_parser = subparsers.add_parser("volume", help="Get/set volume")
    volume_parser.add_argument("level", type=int, nargs="?",
                               help="Volume level (0-320)")

    # Audio device control
    adev_parser = subparsers.add_parser("adev", help="Audio device control")
    adev_parser.add_argument("device_id", nargs="?",
                             help="Device ID to set as active")

    return parser


def handle_command(vlc: VLCRemoteControl, args: CommandLineArgs) -> None:
    """Execute the VLC command based on parsed arguments.

    Args:
        vlc: VLCRemoteControl instance
        args: Parsed command line arguments

    Raises:
        SystemExit: On command execution error
    """
    match args.command:
        # Simple commands without arguments
        case "play" | "stop" | "next" | "prev" | "clear" | "pause" | "quit":
            getattr(vlc, args.command)()

        # Toggle commands that return boolean
        case "repeat" | "loop" | "random":
            result = getattr(vlc, args.command)()
            sys.stdout.write(f"{args.command}: {'on' if result else 'off'}")

        # Status command
        case "status":
            for line in vlc.status():
                sys.stdout.write(line+"\n")

        # Playlist command
        case "playlist":
            for i, item in enumerate(vlc.playlist(), 1):
                sys.stdout.write(f"{i}. {item}\n")

        # Add file command
        case "add":
            vlc.add(args.file)

        # Goto command
        case "goto":
            vlc.goto(args.index)

        # Volume command
        case "volume":
            if args.level is None:
                sys.stdout.write(f"Current volume: {vlc.get_volume()}")
            else:
                vlc.set_volume(args.level)

        # Audio device command
        case "adev":
            if args.device_id is None:
                devices = vlc.get_adev()
                for device in devices:
                    sys.stdout.write(f"{device.id} - {device.name}\n")
            else:
                vlc.set_adev(args.device_id)

        case _:
            sys.exit(f"Error: Unknown command '{args.command}'")


def main() -> None:
    """Entry point for the VLC remote control CLI."""
    parser = create_parser()
    args = parser.parse_args(namespace=CommandLineArgs())

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        vlc = VLCRemoteControl(args.host, args.port)
        handle_command(vlc, args)
    except (FileNotFoundError, ValueError, UnknownRemoteCommand,
            ConnectionError, PausedPlayerError) as e:
        sys.exit(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
