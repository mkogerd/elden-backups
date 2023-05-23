from datetime import datetime
from typing import List
import argparse
import glob
import os
import shutil

# Supported save types
SINGLE_PLAYER = 'singleplayer'
CO_OP = 'coop'
ALL = 'all'

# Savefile extensions associated with save types
TYPE_TO_EXTENSIONS = { 
    CO_OP: ['.co2'],
    SINGLE_PLAYER: ['.sl2'],
    ALL: ['.co2','.sl2'],
}


def parseArgs() -> argparse.Namespace:
    argParser = argparse.ArgumentParser(
        description='A simple program for backing up Elden Ring saves. Supports both vanilla and seamless co-op mod saves.'
    )

    argParser.add_argument('source', help='directory containing Elden Ring save files (.co2, .sl2)')
    argParser.add_argument('-d', '--destination', help='directory to store generated backup directories in (defaults to source directory)')
    argParser.add_argument('-t', '--type', choices=[SINGLE_PLAYER, CO_OP, ALL], default=CO_OP, help=f'save file type to backup (defaults to "{CO_OP}" if not specified)')

    args = argParser.parse_args()
    cleanArgs(args)

    return args


def cleanArgs(args: argparse.Namespace):
    # Modifies args in place
    if not args.destination:
        args.destination = args.source


def backupSaveFiles(source: str, destination: str, type: str):
    fullBackupDirectoryPath = f'{destination}/{generateBackupDirName(type)}'
    os.mkdir(fullBackupDirectoryPath)

    saveFiles = getSaveFiles(source, type)
    for file in saveFiles:
        shutil.copy(file, fullBackupDirectoryPath)


def generateBackupDirName(type: str):
    timestamp = datetime.now().strftime('%Y-%m-%d_T%H%M%S')
    backupDirectory = f'{timestamp}_saveBackups({type})'
    return backupDirectory


def getSaveFiles(source: str, type: str) -> List[str]:
    saveFiles = []
    for extension in TYPE_TO_EXTENSIONS[type]:
        tmp = glob.glob(f'{source}/*{extension}*')
        saveFiles.extend(tmp)

    return saveFiles


args = parseArgs()
backupSaveFiles(args.source, args.destination, args.type)

