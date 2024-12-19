#!/usr/bin/env python3
"""Utility to calc files control sum in specified folder.
    Type --help for command line parameters description."""

import argparse
import pathlib
import sys
import fnmatch
import os
from collections.abc import Iterable

import calc_files_control_sum.my_utils as my_utils
import calc_files_control_sum.my_strings as my_strings
import calc_files_control_sum.str_without_trans as swtrans
import calc_files_control_sum.config as config

MiB_1 = 1024*1024


def process(full_path_to_folder: str, patterns: list, alg: str) -> Iterable[tuple[str, str, int]]:
    """Перечисляет файлы внутри папки, подсчитывая их контрольную сумму,
    получая имя файла и его размер в байтах.
    Функция-генератор"""
    loc_path = pathlib.Path(full_path_to_folder)
    # enumerating files ONLY!!!
    for child in loc_path.iterdir():
        if child.is_file():
            for pattern in patterns:
                if fnmatch.fnmatch(child.name, pattern):
                    # file checksum calculation
                    loc_hash = my_utils.get_hash_file(str(child.absolute()), alg)
                    yield loc_hash, child.name, child.stat().st_size
                    break


# parse_files_info
def parse_control_sum_file(control_sum_filename: str, settings: dict) -> Iterable[tuple[str, str]]:
    """разбор файла на имена файлов и их контрольные суммы!
    Функция-генератор"""
    fld = settings["src"]
    # вычислять CRC не нужно!
    cr = config.ConfigReader(control_sum_filename, check_crc=False)
    for cs_from_file, filename_ext in cr.read(swtrans.str_start_files_header):
        full_file_name = f"{fld}{os.path.sep}{filename_ext.strip()}"
        yield full_file_name, cs_from_file


def check_files(control_sum_filename: str) -> tuple:
    """comparison of the current checksum of the file and the checksum read from the file."""
    # вызов my_utils.settings_from_file проверяет контрольную сумму файла настроек после его открытия
    settings = my_utils.settings_from_file(control_sum_filename, check_crc=True)
    total_tested, modified_files_count, access_errors, total_size = 0, 0, 0, 0
    for loc_fn, old_cs in parse_control_sum_file(control_sum_filename, settings):
        try:
            curr_cs = my_utils.get_hash_file(full_path_to_file=loc_fn, algorithm=settings['alg'])
            # вычисляю общий размер проверенных файлов в байтах
            total_size += my_utils.get_file_stat(loc_fn).st_size
            total_tested += 1
            if curr_cs != old_cs:
                modified_files_count += 1
                # сообщаю пользователю, что файл был проверен, изменения в файле ЕСТЬ!
                print(f"{my_strings.strFileModified}{swtrans.strKeyValueSeparator} {loc_fn}")
            else:
                # сообщаю пользователю, что файл был проверен, изменений в файле нет!
                print(f"{my_strings.strFileChecked}: {loc_fn}")
        except OSError as e:
            access_errors += 1
            print(e)
            continue

    return total_tested, modified_files_count, access_errors, total_size


def main():
    # изменяю кодировку stdout
    sys.stdout.reconfigure(encoding=config.Config.default_encoding)
    """Главная функция"""
    src_folder = my_utils.get_owner_folder_path(sys.argv[0])  # папка с файлами

    parser = argparse.ArgumentParser(description=my_strings.strDescription, epilog=my_strings.strEpilog)
    parser.add_argument("-c", "--check_file", type=str, help=my_strings.strArgCheckFile)
    parser.add_argument("-s", "--src", type=str, help=my_strings.strArgSrc)
    parser.add_argument("-a", "--alg", type=str, help=my_strings.strArgAlg, default="md5")
    parser.add_argument("-e", "--ext", type=str, help=my_strings.strArgExt, default="*.zip")

    args = parser.parse_args()

    # режим проверки файлов включен (!= None)
    if args.check_file and not my_utils.is_file_exist(args.check_file):
        raise ValueError(f"{my_strings.strInvalidCheckFn}: {args.check_file}")

    if args.check_file:
        print(my_strings.strCheckingStarted)
        # текущее время
        dt = my_utils.DeltaTime()
        # проверка файлов по их контрольным суммам
        total_files, modified, access_err, total_size = check_files(args.check_file)
        delta = dt.delta()  # in second [float]
        mib_per_sec = total_size / MiB_1 / delta
        # Итоги проверки файлов по их контрольным суммам
        print(f"{my_strings.strTotalFilesChecked}: {total_files}")
        print(f"{my_strings.strTotalFilesMod}: {modified}")
        print(f"{my_strings.strIOErrors}: {access_err}")
        print(f"{my_strings.strCheckingSpeed}: {mib_per_sec:.3f}")
        sys.exit()  # выход

    if args.src:
        if not my_utils.is_folder_exist(args.src):
            raise ValueError(f"{my_strings.strInvalidSrcFld} {args.src}")
    else:
        args.src = src_folder

    if args.ext:
        # формирование списка расширений для записи в секцию настроек файла
        args.ext = args.ext.replace(" ", "")   # удаляю все пробелы из строки
        args.ext = args.ext.split(",")  # создаю список

    # текущее время
    dt = my_utils.DeltaTime()
    # добавляю в словарь время
    loc_d = vars(args)
    loc_d["start_time"] = str(dt.start_time)

    # сохраняю настройки в stdout
    cw = config.ConfigWriter(filename_or_fileobject=sys.stdout, check_crc=True)
    cw.write_section(swtrans.str_settings_header, loc_d.items())

    total_size = count_files = 0
    # вывод в stdout информации при подсчете контрольных сумм
    cw.write_section(swtrans.str_start_files_header, None)
    for file_hash, file_name, file_size in process(args.src, args.ext, args.alg):
        total_size += file_size  # file size
        count_files += 1
        cw.write_line(f"{file_hash}{swtrans.strCS_filename_splitter}{file_name}")

    cw.write_section(swtrans.str_info_section, None)
    delta = dt.delta()  # in second [float]
    cw.write_line(f"{my_strings.strEnded}: {dt.stop_time}\t{my_strings.strFiles}: {count_files};\t"
                  f"{my_strings.strBytesProcessed}: {total_size}")
    mib_per_sec = total_size / MiB_1 / delta
    cw.write_line(f"{my_strings.strProcSpeed}: {mib_per_sec:.3f}")


if __name__ == '__main__':
    main()
