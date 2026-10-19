import json
import os

BASE_DIR = "/Users/Apple16/Downloads/cetif/editor_specifications"
os.makedirs(BASE_DIR, exist_ok=True)

# 1. Blank Canvas Presets
blank_presets = {
    "certificate_a4_landscape": {
        "name": "Blank Certificate (A4 Landscape)",
        "type": "certificate",
        "paperSize": "A4",
        "orientation": "landscape",
        "dimensions": {
            "physical_mm": {"width": 297, "height": 210},
            "px_96dpi": {"width": 1123, "height": 794},
            "px_editor": {"width": 800, "height": 566},
            "px_hd_print": {"width": 2000, "height": 1414},
            "px_300dpi": {"width": 3508, "height": 2480},
            "aspect_ratio": 1.414
        },
        "background": {"type": "color", "value": "#ffffff"},
        "blocks": [
            {
                "type": "text",
                "style": {
                    "top": "25%",
                    "left": "10%",
                    "width": "80%",
                    "color": "#0F172A",
                    "fontSize": "42em",
                    "fontFamily": "Mukta, sans-serif",
                    "fontWeight": 700,
                    "textAlign": "center"
                },
                "value": "Certificate of Completion",
                "autoScale": True
            },
            {
                "type": "text",
                "style": {
                    "top": "45%",
                    "left": "10%",
                    "width": "80%",
                    "color": "#1E3A8A",
                    "fontSize": "36em",
                    "fontFamily": "Marcellus, serif",
                    "fontWeight": 400,
                    "textAlign": "center"
                },
                "value": "[recipient.name]",
                "autoScale": True
            },
            {
                "type": "text",
                "style": {
                    "top": "60%",
                    "left": "15%",
                    "width": "70%",
                    "color": "#475569",
                    "fontSize": "18em",
                    "fontFamily": "Mukta, sans-serif",
                    "fontWeight": 400,
                    "textAlign": "center"
                },
                "value": "For successfully completing [group.name] on [certificate.issued_on]",
                "autoScale": True
            },
            {
                "type": "qrcode",
                "style": {
                    "top": "75%",
                    "left": "80%",
                    "width": "80px",
                    "height": "80px"
                },
                "data": "[certificate.url]",
                "caption": "Scan to Verify"
            }
        ]
    },
    "certificate_a4_portrait": {
        "name": "Blank Certificate (A4 Portrait)",
        "type": "certificate",
        "paperSize": "A4",
        "orientation": "portrait",
        "dimensions": {
            "physical_mm": {"width": 210, "height": 297},
            "px_96dpi": {"width": 794, "height": 1123},
            "px_editor": {"width": 566, "height": 800},
            "px_hd_print": {"width": 1414, "height": 2000},
            "px_300dpi": {"width": 2480, "height": 3508},
            "aspect_ratio": 0.707
        },
        "background": {"type": "color", "value": "#ffffff"},
        "blocks": []
    },
    "certificate_letter_landscape": {
        "name": "Blank Certificate (US Letter Landscape)",
        "type": "certificate",
        "paperSize": "US_Letter",
        "orientation": "landscape",
        "dimensions": {
            "physical_inches": {"width": 11, "height": 8.5},
            "px_96dpi": {"width": 1056, "height": 816},
            "px_editor": {"width": 800, "height": 618},
            "px_300dpi": {"width": 3300, "height": 2550},
            "aspect_ratio": 1.294
        },
        "background": {"type": "color", "value": "#ffffff"},
        "blocks": []
    },
    "badge_square": {
        "name": "Blank Badge (Square 1:1)",
        "type": "badge",
        "paperSize": None,
        "orientation": None,
        "dimensions": {
            "aspect_ratio": 1.0,
            "px_editor": {"width": 512, "height": 512},
            "px_vector_viewbox": {"width": 1000, "height": 1000}
        },
        "background": {"type": "transparent"},
        "blocks": []
    },
    "transcript_a4": {
        "name": "Blank Transcript (A4 Landscape)",
        "type": "transcript",
        "paperSize": "A4",
        "orientation": "landscape",
        "dimensions": {
            "physical_mm": {"width": 297, "height": 210},
            "px_96dpi": {"width": 1123, "height": 794},
            "aspect_ratio": 1.414
        },
        "background": {"type": "color", "value": "#ffffff"},
        "blocks": []
    },
    "training_record_a4": {
        "name": "Blank Training Record (A4 Landscape)",
        "type": "training_record",
        "paperSize": "A4",
        "orientation": "landscape",
        "dimensions": {
            "physical_mm": {"width": 297, "height": 210},
            "px_96dpi": {"width": 1123, "height": 794},
            "aspect_ratio": 1.414
        },
        "background": {"type": "color", "value": "#ffffff"},
        "blocks": []
    },
    "assessment_a4": {
        "name": "Blank Assessment (A4 Landscape)",
        "type": "assessment",
        "paperSize": "A4",
        "orientation": "landscape",
        "dimensions": {
            "physical_mm": {"width": 297, "height": 210},
            "px_96dpi": {"width": 1123, "height": 794},
            "aspect_ratio": 1.414
        },
        "background": {"type": "color", "value": "#ffffff"},
        "blocks": []
    },
    "letter_a4_portrait": {
        "name": "Blank Letter (A4 Portrait)",
        "type": "letter",
        "paperSize": "A4",
        "orientation": "portrait",
        "dimensions": {
            "physical_mm": {"width": 210, "height": 297},
            "px_96dpi": {"width": 794, "height": 1123},
            "aspect_ratio": 0.707
        },
        "background": {"type": "color", "value": "#ffffff"},
        "blocks": []
    }
}

with open(os.path.join(BASE_DIR, "blank_canvas_presets.json"), "w") as f:
    json.dump(blank_presets, f, indent=2)

# 2. Dynamic Attributes
attributes_data = {
    "recipient": [
        {"tag": "[recipient.name]", "label": "Recipient Full Name", "example": "Jane Doe"}
    ],
    "credential": [
        {"tag": "[certificate.uuid]", "label": "Certificate ID / UUID", "example": "01kktw3bfm6kbfqy5t1e6znnts"},
        {"tag": "[certificate.issued_on]", "label": "Issue Date", "example": "October 19, 2026"},
        {"tag": "[certificate.expired_on]", "label": "Expiration Date", "example": "October 19, 2028"},
        {"tag": "[certificate.url]", "label": "Verification URL", "example": "https://verify.certifier.io/01kktw3bfm6kbfqy5t1e6znnts"}
    ],
    "issuer": [
        {"tag": "[issuer.name]", "label": "Issuer / Organization Name", "example": "Certifier Institute"},
        {"tag": "[issuer.support_email]", "label": "Issuer Support Email", "example": "support@issuer.com"}
    ],
    "group": [
        {"tag": "[group.name]", "label": "Course / Template Title", "example": "Fall Protection Training"},
        {"tag": "[group.description]", "label": "Course Description", "example": "Comprehensive occupational safety certification."}
    ],
    "custom": [
        {"tag": "[custom.<name>]", "label": "Custom User Attribute", "description": "Arbitrary variable specified per recipient (e.g. [custom.grade], [custom.instructor])"}
    ]
}

with open(os.path.join(BASE_DIR, "dynamic_attributes.json"), "w") as f:
    json.dump(attributes_data, f, indent=2)

# 3. Typography & 58 Google Fonts
typography_data = {
    "presets": {
        "heading": {"fontFamily": "Mukta, sans-serif", "fontSize": "30px", "fontWeight": 700, "lineHeight": 1.2},
        "subheading": {"fontFamily": "Mukta, sans-serif", "fontSize": "24px", "fontWeight": 700, "lineHeight": 1.3},
        "body": {"fontFamily": "Mukta, sans-serif", "fontSize": "16px", "fontWeight": 400, "lineHeight": 1.5}
    },
    "supportedWeights": [100, 200, 300, 400, 500, 600, 700, 800, 900, 950, 1000],
    "googleFonts": {
        "sans": [
            "Bricolage Grotesque", "Cairo", "DM Sans", "Golos", "Google Sans Flex",
            "Gothic A1", "Hind Madurai", "Inter", "Inter Tight", "Josefin Sans",
            "Kufam", "Lato", "Lexend", "Manrope", "Montserrat", "Mullish",
            "Noto Sans", "Open Sans", "Oswald", "Outfit", "Poppins", "Prompt",
            "Quicksand", "Roboto", "Teko", "Tenor Sans", "Ubuntu"
        ],
        "serif": [
            "Barlow Condensed", "Baskervville", "Bellefair", "Cinzel", "Cormorant",
            "EB Garamond", "Inika", "Josefin Slab", "Kameron", "Libre Baskerville",
            "Lora", "Marcellus", "Merriweather", "Newsreader", "Noto Serif Display",
            "Playfair Display", "PT Serif", "Roboto Slab"
        ],
        "handwriting": [
            "Alex Brush", "Birthstone", "Bokor", "Dancing Script", "Ephesis",
            "Great Vibes", "Kalam", "Lobster", "Marck Script", "Monte Carlo",
            "Satisfy", "Whisper"
        ],
        "mono": ["Space Mono"]
    }
}

with open(os.path.join(BASE_DIR, "typography_and_fonts.json"), "w") as f:
    json.dump(typography_data, f, indent=2)

# 4. QR Code Specifications
qr_specs = {
    "type": "qrcode",
    "modes": {
        "verification_page": {
            "default_data": "[certificate.url]",
            "default_caption": "Scan to Verify",
            "caption_style": {"fontSize": "14em", "color": "#858585", "fontFamily": "Mukta, sans-serif"}
        },
        "custom_url": {
            "default_data": "https://example.com",
            "default_caption": "Visit Website"
        }
    },
    "rendering": {
        "format": "vector_svg",
        "errorCorrection": "M",
        "aspectRatioLocked": True,
        "default_size": "80x80px"
    }
}

with open(os.path.join(BASE_DIR, "qr_code_specs.json"), "w") as f:
    json.dump(qr_specs, f, indent=2)

print("Saved all editor specifications and blank presets into:", BASE_DIR)
