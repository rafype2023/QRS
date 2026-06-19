#!/usr/bin/env python3
import os
import sys
import subprocess

# Auto-install dependencies if missing
try:
    import qrcode
    from PIL import Image
except ImportError:
    print("Las dependencias necesarias ('qrcode' y/o 'pillow') no están instaladas.")
    print("Instalándolas automáticamente en el entorno local...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "qrcode", "pillow"])
        import qrcode
        from PIL import Image
        print("¡Instalación exitosa!\n")
    except Exception as e:
        print(f"Error al instalar las dependencias: {e}")
        print("Por favor, ejecuta manualmente: pip install qrcode pillow")
        sys.exit(1)

import argparse

def generate_qrs(base_url, output_dir):
    # Ensure base_url ends with a slash
    if not base_url.endswith('/'):
        base_url += '/'

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List of profiles to generate QRs for
    profiles = [
        {"name": "ada", "file": "ada.html"},
        {"name": "diego", "file": "diego.html"},
        {"name": "fernan", "file": "fernan.html"},
        {"name": "yoisa", "file": "yoisa.html"},
        {"name": "boxeo", "file": "boxeo.html"},
        {"name": "vane", "file": "vane.html"},
        {"name": "yariel", "file": "yariel.html"},
    ]

    print(f"Generando códigos QR apuntando a la URL base: {base_url}")
    print("-" * 60)

    for p in profiles:
        target_url = f"{base_url}{p['file']}"
        output_path = os.path.join(output_dir, f"{p['name']}_qr.png")
        
        # Configure QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(target_url)
        qr.make(fit=True)

        # Generate image (white background, very dark blue foreground for high contrast and elegant design)
        img = qr.make_image(fill_color="#080710", back_color="#FFFFFF")
        img.save(output_path)
        
        print(f"✔ Generado: {output_path}")
        print(f"  Enlace: {target_url}\n")

    print("-" * 60)
    print(f"¡Todos los códigos QR han sido generados exitosamente en la carpeta '{output_dir}/'!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de códigos QR para credenciales de perfiles.")
    parser.add_argument(
        "--url", 
        type=str, 
        default="https://ejemplo.com/credenciales/", 
        help="URL base donde se alojarán las páginas estáticas. (Ej: https://misitio.com/credenciales/)"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="qrcodes", 
        help="Nombre de la carpeta de salida para los códigos QR."
    )
    args = parser.parse_args()

    # If default URL is used, remind the user they can customize it
    if args.url == "https://ejemplo.com/credenciales/":
        print("Nota: Usando la URL base predeterminada (https://ejemplo.com/credenciales/).")
        print("Puedes cambiarla usando el parámetro --url, por ejemplo:")
        print("  python3 generate_qrs.py --url https://minegocio.com/perfiles/\n")

    generate_qrs(args.url, args.output)
