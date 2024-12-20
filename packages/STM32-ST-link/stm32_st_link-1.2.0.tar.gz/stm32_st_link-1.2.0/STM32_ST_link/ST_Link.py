#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/12 下午3:06
# @Author  : 周梦泽
# @File    : ST_Link.py
# @Software: PyCharm
# @Description:STM32_ST-Link-CLI单片机操作：连接、烧录、擦除，使用前必须安装STM32 ST-LINK Utility
import platform
import subprocess
import os
from typing import Optional, List, Tuple
import logging
from .libs.find_folder import find_folder


class STLinkCLI:
    """
    ST-LINK CLI命令行工具的Python封装类
    """

    def __init__(self, logging_level: int = logging.INFO):
        """
        初始化ST-LINK CLI封装类

        Args:
            logging_level: 日志级别
        """
        # 配置日志
        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('STLinkCLI')

        # 获取ST-LINK CLI工具绝对路径
        self.current_dir = os.path.dirname(__file__)
        self.cli_path = os.path.join(self.current_dir, 'ST_Link_CLI/ST-LINK_CLI.exe')
        # 查找驱动文件夹，判断是否已经安装对应的驱动
        if not find_folder(base_path=r"C:\Windows\System32\DriverStore\FileRepository",
                           target_prefix="stlink_dbg_winusb.inf") or not find_folder(
            base_path=r"C:\Windows\System32\DriverStore\FileRepository", target_prefix="stlink_vcp.inf"):
            self.logger.info("Please install the driver for the ST-LINK device")
            self.install_driver()

    def _execute_command(self, command: List[str], timeout: int = 60) -> Tuple[int, str, str]:
        """
        执行ST-LINK CLI命令

        Args:
            command: 完整的命令参数列表

        Returns:
            (返回码, 标准输出, 标准错误)的元组
        """
        try:
            self.logger.info(f"Execute command:{command}")
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='replace'
            )

            stdout, stderr = process.communicate(timeout=timeout)
            return process.returncode, stdout, stderr
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            raise

    def connect(self, serial_number: Optional[str] = None, timeout: int = 1 * 60) -> bool:
        """
        连接到ST-LINK设备

        Args:
            serial_number: ST-LINK设备序列号(可选)
            timeout: 超时时间

        Returns:
            连接是否成功
        """
        command = [self.cli_path, "-c"]
        if serial_number:
            command.extend(["-SN", serial_number])

        return_code, stdout, stderr = self._execute_command(command, timeout=timeout)
        success = return_code == 0

        if success:
            self.logger.info("Successfully connected to ST-LINK device")
        else:
            self.logger.error(f"Failed to connect to ST-LINK device: {stderr}")

        return success

    def program(self,
                bin_path: str,
                stldr_path: str = None,
                address: Optional[str] = None,
                verify: bool = True,
                reset: bool = True,
                timeout: int = 1 * 60) -> bool:
        if not os.path.exists(bin_path):
            raise FileNotFoundError(f"Program file not found: {bin_path}")
        self.logger.info("Start burning programming")
        command = [self.cli_path, "-P", bin_path]

        if address:
            command.extend([address])
        if stldr_path:
            if not os.path.exists(stldr_path):
                raise FileNotFoundError(f"Program file not found: {stldr_path}")
            command.extend(["-EL", stldr_path])
        if verify:
            command.append("-V")
        if reset:
            command.append("-Rst")

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='gbk',  # 修改为GBK编码，兼容中文编码
                errors='replace',  # 替换无法解码的字符
                text=True,
                bufsize=1,
                universal_newlines=True,
            )
            stdout, stderr = process.communicate(timeout=timeout)
            return_code = process.poll()

            success = return_code == 0

            if success:
                self.logger.info(f"Successfully programmed file: {bin_path}")
                if stdout:
                    self.logger.info(f"Program output: {stdout}")
                if stderr:
                    self.logger.info(f"Program error: {stderr}")
            else:
                self.logger.error(f"Programming failed. Return code: {return_code}")
                if stdout:
                    self.logger.error(f"Program output: {stdout}")
            return success

        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            raise

    def verify(self, bin_path: str, address: Optional[str] = None, timeout: int = 1 * 60) -> bool:
        """
        验证操作

        Args:
            bin_path: 要验证的二进制文件路径
            address: 起始地址(可选)
            timeout: 超时时间

        Returns:
            验证是否成功
        """
        if not os.path.exists(bin_path):
            raise FileNotFoundError(f"Verify file not found: {bin_path}")

        command = [self.cli_path, "-V", bin_path]
        if address:
            command.extend(["-P", address])

        return_code, stdout, stderr = self._execute_command(command, timeout=timeout)
        success = return_code == 0

        if success:
            self.logger.info(f"Successfully verified file: {bin_path}")
        else:
            self.logger.error(f"Verification failed: {stderr}")

        return success

    def erase(self, start_addr: Optional[str] = None, size: Optional[str] = None, timeout: int = 1 * 60) -> bool:
        """
        擦除操作

        Args:
            start_addr: 起始地址(可选)
            size: 擦除大小(可选)
            timeout: 超时时间

        Returns:
            擦除是否成功
        """
        command = [self.cli_path, "-ME"]

        if start_addr and size:
            command.extend(["-S", start_addr, size])
        return_code, stdout, stderr = self._execute_command(command, timeout=timeout)
        success = return_code == 0

        if success:
            self.logger.info("Successfully erased memory")
        else:
            self.logger.error(f"Erase operation failed: {stderr}")

        return success

    def reset(self, timeout: int = 1 * 60) -> bool:
        """
        复位目标设备

        Returns:
            复位操作是否成功
        """
        command = [self.cli_path, "-Rst"]
        return_code, stdout, stderr = self._execute_command(command, timeout=timeout)
        success = return_code == 0

        if success:
            self.logger.info("Successfully reset target")
        else:
            self.logger.error(f"Reset operation failed: {stderr}")

        return success

    def install_driver(self):
        # 获取处理器架构信息
        # run_as_admin()
        processor_architecture = platform.machine().upper()

        # 判断是否是64位系统
        is_64bit = processor_architecture.endswith('64')

        # 根据架构选择合适的安装程序
        if is_64bit:
            installer = os.path.join(self.current_dir, 'ST-LINK_USB_V2_1_Driver/dpinst_amd64.exe')
        else:
            installer = os.path.join(self.current_dir, 'ST-LINK_USB_V2_1_Driver/dpinst_x86.exe')
        self.logger.info(f"Starting installation with {installer}...")
        os.startfile(installer)
        raise RuntimeError("Please complete the installation of the driver")
