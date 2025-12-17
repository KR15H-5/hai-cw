import subprocess
import shutil

# Create QR code text lines for the given data or return a simple fallback
def generate_qr_code(data):

    if not shutil.which('qrencode'):
        return [
            "  ████████████████  ",
            "  ██ ▄▄▄▄▄ █ ▄██  ",
            "  ██ █   █ █▀▀██  ",
            "  ██ █▄▄▄█ █▄ ██  ",
            "  ██▄▄▄▄▄▄▄█▄▄██  ",
            "  ████████████████  "
        ]
    
    result = subprocess.run(
        ['qrencode', '-t', 'UTF8', str(data)],
        capture_output=True,
        text=True,
        check=True
    )
    
    qr_lines = result.stdout.strip().split('\n')
    return qr_lines
        


# Build a formatted ticket string with booking and QR code details
def generate_ticket(ref, customer, movie, date, time, seats, tickets, total):

    WIDTH = 46

    # Helper to wrap a line of text inside a box border
    def box(text=""):
        text = text[:WIDTH]            
        text = text.ljust(WIDTH)       
        return f"┃ {text} ┃"

    
    qr_data = f"{ref}"
    qr_lines = generate_qr_code(qr_data)

    
    seat_str = ', '.join([f"{s[0]}{s[1]}" for s in seats])


    movie_display = movie[:23] + '...' if len(movie) > 25 else movie

    ticket = "\n"
    ticket += f"┏{'━' * (WIDTH + 2)}┓\n"
    ticket += box("SAVOYBOT TICKET") + "\n"
    ticket += f"┣{'━' * (WIDTH + 2)}┫\n"
    ticket += box(f"REF: {ref:<13} [User] {customer:<18}") + "\n"
    ticket += box(f"{movie_display:<23} * 12A") + "\n"
    ticket += box(f"{date:<18}      {time:<10}") + "\n"
    ticket += box(f"{seat_str:<17} TKT x{tickets}   £{total:.2f}") + "\n"
    ticket += f"┣{'━' * (WIDTH + 2)}┫\n"
    ticket += box("SCAN AT ENTRANCE:") + "\n"

    # Centre each QR code line
    for qr_line in qr_lines:
        centred = qr_line.center(WIDTH)
        ticket += box(centred) + "\n"

    ticket += f"┣{'━' * (WIDTH + 2)}┫\n"
    ticket += box("123 Savoy St, Nottingham NG1 1AA") + "\n"
    ticket += box("Present this ticket • Enjoy your movie!") + "\n"
    ticket += f"┗{'━' * (WIDTH + 2)}┛\n"

    return ticket


if __name__ == "__main__":
    pass
