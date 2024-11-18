import io

def last_lines(file_path, buffer_size=io.DEFAULT_BUFFER_SIZE):
    
    # rb abre arquivo como bytes
    with open(file_path, 'rb') as file:
        file.seek(0, io.SEEK_END)  # Vai para o final do arquivo
        position = file.tell()  # Obtém o tamanho total do arquivo
        buffer = b""
        
        while position > 0:
            # Define o tamanho do chunk a ser lido
            chunk_size = min(buffer_size, position)
            position -= chunk_size
            file.seek(position, io.SEEK_SET)
            chunk = file.read(chunk_size) + buffer
            buffer = b""
            
            # Processa o chunk de trás para frente
            lines = chunk.split(b'\n')
            buffer = lines.pop(0)  # O restante pode ser uma linha incompleta
            
            for line in reversed(lines):
                yield line.decode('utf-8') + '\n'  # Decodifica e retorna a linha completa
        
        # Retorna qualquer sobra como última linha
        if buffer.strip():
            yield buffer.decode('utf-8') + '\n'


for line in last_lines('my_file.txt'):
    print(line, end='')
