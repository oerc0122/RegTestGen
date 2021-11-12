def writeln(*line, file=None, indent=0, **kwargs):
    file.write((" "*3*indent)+"".join(line)+'\n')
