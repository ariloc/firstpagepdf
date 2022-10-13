import sys
import os
import PyPDF2

def exportPdfs (inputPath, outputPath):
    cnt = 0
    for filename in os.listdir(inputPath):
        actPath = os.path.join(inputPath, filename)

        if (not os.path.isfile(actPath)):
            continue

        try:
            inputObj = open(actPath, "rb")
            pdfReader = PyPDF2.PdfFileReader(inputObj)
        except PyPDF2.utils.PdfReadError:
            print(f"{actPath} is not a valid PDF file. Skipping...\n")
            continue
        except Exception:
            print(f"Unknown error. Skipping {actPath}...")
            continue

        firstPage = pdfReader.getPage(0)

        output = PyPDF2.PdfFileWriter()
        output.addPage(firstPage)
        outPathFile = os.path.join(outputPath, filename)

        if (os.path.exists(outPathFile)):
            print(f"Output path already exists. Skipping export of file at {actPath}...")
            inputObj.close()
            continue

        outputObj = open(outPathFile, "wb")
        output.write(outputObj)
        outputObj.close()

        inputObj.close()

        cnt += 1
        print(f"{cnt} files successfully processed.")


if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print('Syntax: python firstpagepdf.py INPUT_PATH OUTPUT_PATH')
        exit(1)
    if (not os.path.isdir(sys.argv[1]) or not os.access(sys.argv[1], os.R_OK)):
        print('The input path doesn\'t exist, isn\'t a directory or isn\'t readable')
        exit(1)
    if (not os.path.isdir(sys.argv[2]) or not os.access(sys.argv[2], os.X_OK | os.W_OK)):
        print('The output path doesn\'t exist or isn\'t a directory or isn\'t writable')
        exit(1)
    if (os.path.samefile(sys.argv[1], sys.argv[2])):
        print('Output and input directories must be distinct')
        exit(1)

    exportPdfs(sys.argv[1], sys.argv[2])
    print('Done!')
