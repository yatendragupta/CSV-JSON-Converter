import configparser
import Logger
import Converter

# Read Config file
config = configparser.SafeConfigParser()
config.read('config.ini')
csvFile = config.get('Csv2Json','csvInputFile')
jsonFile = config.get('Csv2Json','csvOutputFile')
loggerFile = config.get('Csv2Json','LoggerFile')
debugLvl = config.get('Csv2Json','LogLevel')

def main():
    # Initialising Log File
    Logger.init(loggerFile, debugLvl)

    # Call the CSV to JSON function
    Converter.convertToJson(csvFile, jsonFile)

if __name__ == '__main__':
    main()