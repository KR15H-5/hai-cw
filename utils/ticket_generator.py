import subprocess
import shutil

def generate_qr_code(data):
    """Generate QR code using qrencode command"""
    try:
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
        
    except Exception:
        return [
            "  ████████████████  ",
            "  ██          ██  ",
            "  ██  QR CODE ██  ",
            "  ██          ██  ",
            "  ████████████████  "
        ]


def generate_ticket(ref, customer, movie, date, time, seats, tickets, total):
    """Generate compact ASCII ticket with real QR code"""

    WIDTH = 46

    def box(text=""):
        text = text[:WIDTH]            # enforce max width
        text = text.ljust(WIDTH)       # pad to width
        return f"┃ {text} ┃"

    # QR data
    qr_data = f"{ref}"
    qr_lines = generate_qr_code(qr_data)

    # Seat string
    seat_str = ', '.join([f"{s[0]}{s[1]}" for s in seats])

    # Truncate movie
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
    print("\n" + "="*50)
    print("TESTING TICKET GENERATOR")
    print("="*50)
    
    ticket = generate_ticket(
        ref="BK61868",
        customer="Krish",
        movie="Superman",
        date="Tue, 02 Dec 2025",
        time="11:00",
        seats=[('C', 1), ('C', 2), ('C', 3)],
        tickets=3,
        total=40.50
    )

    print(ticket)

    print("\n" + "="*50)
    print("TICKET GENERATED!")
    print("="*50 + "\n")
