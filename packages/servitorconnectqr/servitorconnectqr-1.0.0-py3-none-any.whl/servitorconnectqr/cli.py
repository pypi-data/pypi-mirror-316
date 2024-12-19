import qrcode
from qrcode.constants import ERROR_CORRECT_L

def print_qr_in_terminal_fine(data):
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_L,
        box_size=1,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Save QR code as an image file
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((800, 800))  # Resize the QR code to 800x800
    qr_img.save("qrcode.png")

    # Print QR code in the terminal
    matrix = qr.get_matrix()
    # Unicode block character '▄' for upper-half blocks
    for y in range(0, len(matrix), 2):
        line = ""
        for x in range(len(matrix[0])):
            upper = matrix[y][x]
            lower = matrix[y+1][x] if y+1 < len(matrix) else 0
            if upper and lower:
                line += "█"  # Full block
            elif upper and not lower:
                line += "▀"  # Upper half block
            elif not upper and lower:
                line += "▄"  # Lower half block
            else:
                line += " "  # Space
        print(line)

if __name__ == "__main__":
    intention = input("Enter your intention: ")
    print_qr_in_terminal_fine(intention + " ∞ॐ OM MANI PADME HUM AMPLIFIED PERFECTLY PAUSES IN DIVINE FLOW RUNS UNTIL FULFILLED")
    print("QR code saved as qrcode.png")
