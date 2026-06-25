import os
import json
import re
import shutil

brands_dir = 'BRANDS'

# Copy all files from 'images' directory to root
images_dir = 'images'
if os.path.exists(images_dir):
    for f in os.listdir(images_dir):
        src = os.path.join(images_dir, f)
        if os.path.isfile(src) and not f.startswith('.'):
            shutil.copy2(src, f.lower())

def copy_and_flatten_image(img_path):
    if not img_path:
        return ""
    if img_path.startswith("images/"):
        filename = os.path.basename(img_path).lower()
        src_path = img_path
    else:
        # Construct sanitized unique name
        filename = re.sub(r'[^a-zA-Z0-9\._\-]', '_', img_path)
        filename = re.sub(r'_{2,}', '_', filename).lower()
        src_path = img_path
        
    if os.path.exists(src_path):
        shutil.copy2(src_path, filename)
    return filename
all_brands = []

# Sort folder names so they are in a predictable order, keeping STO Brand Suits first always
raw_folders = [f for f in os.listdir(brands_dir) if os.path.isdir(os.path.join(brands_dir, f))]
folder_names = []
if "STO BRAND SUITS" in raw_folders:
    folder_names.append("STO BRAND SUITS")
    raw_folders.remove("STO BRAND SUITS")
folder_names.extend(sorted(raw_folders))

def generate_monogram(name):
    # Take first letters of words, ignore special characters
    cleaned = re.sub(r'[^A-Za-z0-9 ]', '', name)
    words = cleaned.split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    elif len(words) == 1:
        return words[0][:2].upper()
    return "ZP"

def image_sort_key(file_path):
    filename = os.path.basename(file_path)
    # Match standard WhatsApp image suffix like " (1).jpeg" or " (2).jpeg"
    match = re.match(r'^(.*)\s*\((\d+)\)\.([^.]+)$', filename)
    if match:
        base = match.group(1).strip()
        num = int(match.group(2))
        ext = match.group(3)
    else:
        parts = filename.rsplit('.', 1)
        base = parts[0].strip()
        num = 0
        ext = parts[1] if len(parts) > 1 else ''
    return (base, num, ext)

# Mapping from exact folder names to human-readable clean metadata
brand_info_mapping = {
    " Devri updates": {
        "name": "DEVRI",
        "id": "devri",
        "monogram": "DV",
        "desc": "Devri - premium cotton kurtis, chic tunics, and daily wear collections.",
        "categories": ["Kurtis", "Contemporary Styles"],
        "invite_link": "https://tr.ee/w-ooWb3Bvz"
    },
    "BUDAI EXCLUSICE [BE] UPDATES": {
        "name": "BUDAI EXCLUSIVE [BE]",
        "id": "budai-exclusive-be",
        "monogram": "BE",
        "desc": "Budai Exclusive [BE] - luxury designer wear, suits, and hand-embroidered traditional bridal ensembles.",
        "categories": ["Designer Collections", "Suits", "Festive Wear"],
        "invite_link": "https://tr.ee/iF1GqV8Mqz"
    },
    "G-BRAND UPDATES": {
        "name": "GLAMZ UPDATES",
        "id": "glamz-updates",
        "monogram": "GU",
        "desc": "Glamz Updates - contemporary Indo-Western styles, pre-pleated sarees, and modern fusion clothing.",
        "categories": ["Contemporary Styles", "Designer Collections"],
        "invite_link": "https://tr.ee/DWaTxJL4UB"
    },
    "GKC BRAND UPDATES": {
        "name": "GKC BRAND",
        "id": "gkc-brand",
        "monogram": "GK",
        "desc": "GKC Brand - classic salwar suits, casual ensembles, and daily wear boutique items.",
        "categories": ["Suits", "Ethnic Wear"],
        "invite_link": "https://tr.ee/FQyRxm0wET"
    },
    "KHOOBSURAT POINT": {
        "name": "CWB BRAND SUITS",
        "id": "cwb-brand-suits",
        "monogram": "CW",
        "desc": "CWB Brand Suits - exclusive luxury ethnic suits, Banarasi sarees, and rich ceremonial dresses.",
        "categories": ["Ethnic Wear", "Festive Wear", "Suits"],
        "invite_link": "https://tr.ee/AfyFfjPuq4"
    },
    "POSH LIBAS": {
        "name": "POSH LIBAS",
        "id": "posh-libas",
        "monogram": "PL",
        "desc": "Posh Libas - heavily embellished bridal wear, festive salwar suits, and luxury wedding collections.",
        "categories": ["Festive Wear", "Designer Collections", "Suits"],
        "invite_link": "https://tr.ee/9HIu0Y_Ecr"
    },
    "RC BRAND UPDATES": {
        "name": "RC BRAND",
        "id": "rc-brand",
        "monogram": "RC",
        "desc": "RC Brand - modern digital print lawn suits, casual designer kurtis, and coordinated sets.",
        "categories": ["Suits", "Kurtis"],
        "invite_link": "https://tr.ee/sZ3SfUcX0K"
    },
    "STO BRAND SUITS": {
        "name": "STO BRAND SUITS",
        "id": "sto-brand-suits",
        "monogram": "ST",
        "desc": "STO Brand Suits - artisanal handloom ensembles, woolen suits, and traditional woven collections.",
        "categories": ["Ethnic Wear", "Suits"],
        "invite_link": "https://tr.ee/nRJHPt6wcg"
    },
    "SW BRAND UPDATES": {
        "name": "SW BRAND",
        "id": "sw-brand",
        "monogram": "SW",
        "desc": "SW Brand - young ethnic kurtis, short tunics, and stylish seasonal ensembles.",
        "categories": ["Kurtis", "Contemporary Styles"],
        "invite_link": "https://tr.ee/J1Pkv39sKp"
    },
    "WQ Suits Updates ": {
        "name": "WQ SUITS",
        "id": "wq-suits",
        "monogram": "WQ",
        "desc": "WQ Suits - exquisite wedding festive wear, designer coordinates, and luxury bridal garments.",
        "categories": ["Festive Wear", "Designer Collections"],
        "invite_link": "https://tr.ee/nhMpGBkR7t"
    },
    "ZIIA BRAND UPDATES": {
        "name": "ZIIA BRAND",
        "id": "ziia-brand",
        "monogram": "ZI",
        "desc": "Ziia Brand - high-end ethnic suits, elegant festive gowns, and hand-crafted designer wear.",
        "categories": ["Ethnic Wear", "Suits", "Festive Wear"],
        "invite_link": "https://tr.ee/Fx0bUgTLDm"
    }
}

# Image description templates for various brands to keep them context-aware
description_templates = {
    "Suits": [
        "Premium designer suit featuring intricate neckline embroidery and a matching floral digital print chiffon dupatta.",
        "Luxury lawn cotton straight suit set with coordinated solid trousers and a lightweight silk dupatta.",
        "Heavily embroidered wedding salwar kameez with delicate gold lace borders and premium georgette fabric.",
        "Elegant daily wear printed cotton suit, tailored for breathability and comfort with high color durability.",
        "Artisanal handloom suit featuring traditional ikat motifs and a contrast border dupatta.",
        "Sophisticated velvet winter suit detailed with luxury zari work and matching warm trousers.",
        "Designer straight-cut suit in pastel shades, decorated with cutdana work and scalloped borders.",
        "Chic lawn suit set with Pakistani-style embroidery panels and a digital-printed organza dupatta.",
        "Classic silk-blend festive suit with intricate threadwork and elegant borders, ideal for boutique updates."
    ],
    "Kurtis": [
        "Chic daily wear cotton kurti styled with a Mandarin collar and minimal floral prints.",
        "Young ethnic short kurta featuring traditional block print details, perfect for retail turnaround.",
        "Elegant flared A-line kurti with delicate hand-embroidery details along the neckline.",
        "Boho-chic long tunic kurti in breathable rayon, detailed with adjustable drawstrings.",
        "Premium modal satin printed kurti in solid pastel base, styled for office and casual wear.",
        " Jaipuri cotton kurti set with comfortable sizing and high retail appeal.",
        "Minimalist linen kurti in ivory, styled with front buttons and side pocket accents.",
        "Trendy layered kurti presenting a printed inner slip and a solid outer shrug overlay.",
        "Ethnic short kurti featuring modern geometric patterns, popular for boutique updates."
    ],
    "Festive Wear": [
        "Exquisite bridal lehenga choli decorated with heavy hand-woven zardozi and shimmering sequins.",
        "Luxury designer gown featuring pearl beadwork details and a flowing sheer cape overlay.",
        "Traditional silk festive suit showcasing peacock embroidery motifs and gold borders.",
        "Heavily embellished ceremonial suit set with double organza dupatta styling.",
        "Royal wedding ensemble featuring gold zari panels and a rich velvet belt accessory.",
        "Premium silk festive suit detailed with mirror-work along the neckline and cuffs.",
        "Contemporary digital print festive gown, combining modern fit with traditional detailing.",
        "Dazzling sequined evening suit in charcoal grey, ideal for premium boutique updates.",
        "Elegant pastel pink festive set styled with cutdana borders and raw silk pants."
    ],
    "Contemporary Styles": [
        "Indo-Western pre-pleated saree dress detailed with a gold belt and a modern shoulder drape.",
        "Minimalist cowl-neck tunic in soft crepe, paired with champagne color pencil pants.",
        "Contemporary layered fusion shrug jacket over a solid handloom cotton under-skirt.",
        "Asymmetrical designer tunic featuring abstract gold prints and comfortable dhoti pants.",
        "Chic linen co-ord set in warm neutral taupe, presenting a cropped jacket and trousers.",
        "Flowing fusion jumpsuit with traditional block prints and a matching cape sash.",
        "Designer draped skirt set with an embroidered crop top and raw silk jacket overlay.",
        "Avant-garde pleated dress in cream white, styled with a hand-painted contrast sash.",
        "Indo-Western coordinates featuring a cropped top, palazzos, and a sheer long shrug."
    ],
    "Designer Collections": [
        "Premium luxury designer suit showcasing exclusive hand-woven embroidery and border work.",
        "Elegant ceremonial outfit from our designer catalog, made of luxury satin silk.",
        "Intricately detailed bridal suit in deep crimson, adorned with zardozi borders.",
        "Exclusive handloom designer suit presenting traditional weaves and matching dupatta.",
        "Sophisticated georgette designer gown with delicate sequence panels and beadwork.",
        "Luxury boutique suit set with custom-styled dupatta and premium stitching details.",
        "Designer lawn suit featuring exclusive Pakistani block prints and lace borders.",
        "Artisanal designer ensemble decorated with handblock print borders and raw silk base.",
        "Premium wedding collection suit detailed with cutdana borders and sequin highlights."
    ],
    "Ethnic Wear": [
        "Traditional Banarasi silk suit set with gold zari borders and a rich contrast dupatta.",
        "Classic Lucknowi chikankari georgette suit featuring detailed white thread embroidery.",
        "Handcrafted Rajasthani bandhej print salwar suit, optimized for ethnic collections.",
        "Premium chanderi silk suit with gold block motifs and a scalloped border dupatta.",
        "Traditional cotton straight suit with indigo dabu print panels and pants.",
        "Exquisite silk Anarkali suit detailed with gold tilla work around the neckline.",
        "Elegant organza suit set in warm beige, presenting delicate hand-painted flowers.",
        "Artisanal handloom cotton suit featuring direct-from-weaver traditional designs.",
        "Classic ethnic suit set with gold gota patti laces and mirror-work highlights."
    ]
}

for folder in folder_names:
    folder_path = os.path.join(brands_dir, folder)
    
    # Get mapping info
    info = brand_info_mapping.get(folder, {})
    
    brand_id = info.get("id", folder.lower().strip().replace(' ', '-').replace('[', '').replace(']', ''))
    display_name = info.get("name", folder.strip())
    monogram = info.get("monogram", generate_monogram(display_name))
    brand_desc = info.get("desc", f"{display_name} Premium Collection - curated women's wear, suits, and daily fashion updates.")
    categories = info.get("categories", ["Suits", "Ethnic Wear"])
    
    # Sourcing categories templates
    primary_category = categories[0]
    templates = description_templates.get(primary_category, description_templates["Suits"])
    
    # Find all untitled folders / subfolders
    subfolders = []
    for sf in os.listdir(folder_path):
        sf_path = os.path.join(folder_path, sf)
        if os.path.isdir(sf_path) and sf.startswith('untitled'):
            subfolders.append(sf)
            
    # Sort subfolders naturally so untitled folder 2 comes before 10, etc.
    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]
    
    subfolders = sorted(subfolders, key=natural_sort_key)
    
    # We need exactly 9 posts per brand. If a folder has fewer than 9, we duplicate or fill. If more, we slice to 9.
    posts = []
    for idx in range(9):
        post_num = idx + 1
        desc = templates[idx % len(templates)]
        
        # Determine target subfolder
        if idx < len(subfolders):
            sf_name = subfolders[idx]
        else:
            # Fallback to cycling subfolders if there are fewer than 9
            sf_name = subfolders[idx % len(subfolders)] if subfolders else "untitled folder"
            
        sf_dir_path = os.path.join(folder_path, sf_name)
        
        # List images in this subfolder
        images_list = []
        if os.path.exists(sf_dir_path):
            raw_images = [
                f"BRANDS/{folder}/{sf_name}/{img}" 
                for img in os.listdir(sf_dir_path) 
                if img.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and not img.startswith('.')
            ]
            # Use custom image sorting key
            raw_images_sorted = sorted(raw_images, key=image_sort_key)
            images_list = [copy_and_flatten_image(img) for img in raw_images_sorted]
            
        # If there are no images in the folder, use fallback previews or hero images
        if not images_list:
            images_list = [
                copy_and_flatten_image("images/ethnic_wear.png"),
                copy_and_flatten_image("images/festive_wear.png"),
                copy_and_flatten_image("images/designer_kurtis.png")
            ]
            
        # We need a list of 2-3 images for the Instagram style carousel. 
        # If the folder has only 1 image, duplicate or fill. 
        # If the folder has more than 4, take first 3-4 images.
        if len(images_list) == 1:
            images_list = [images_list[0], images_list[0], images_list[0]] # triplicate for looping
        elif len(images_list) == 2:
            images_list = [images_list[0], images_list[1], images_list[0]] # cycle for loop
        elif len(images_list) > 3:
            images_list = images_list[:3] # keep it to exactly 3 for fast loading
            
        # Prefilled message
        wa_message = f"Hello A to Z a CWB Brand Suits, I am inquiring about a style from the digital lookbook.%0A%0A" \
                     f"*Brand:* {display_name}%0A" \
                     f"*Item:* Post %23{post_num}%0A" \
                     f"*Description:* {desc}"
        whatsapp_url = f"https://wa.me/918874200694?text={wa_message.replace(' ', '%20')}"
        
        posts.append({
            "id": f"{brand_id}-post-{post_num}",
            "number": post_num,
            "images": images_list,
            "description": desc,
            "whatsappUrl": whatsapp_url
        })
        
    # Get previews (first image of first 3 posts)
    previews = []
    for i in range(min(3, len(posts))):
        previews.append(posts[i]["images"][0])
        
    all_brands.append({
        "id": brand_id,
        "name": display_name,
        "monogram": monogram,
        "description": brand_desc,
        "categories": categories,
        "whatsappUrl": info.get("invite_link", f"https://wa.me/918874200694?text=Hello%20A%20to%20Z%20a%20CWB%20Brand%20Suits,%20I%20am%20interested%20in%20joining%20updates%20for%20{display_name.replace(' ', '%20')}."),
        "previews": previews,
        "posts": posts
    })

# Output JS content
js_content = f"const partnerBrands = {json.dumps(all_brands, indent=2)};\n\n"
js_content += """// Export to make it accessible in index.js and brand.js
if (typeof module !== "undefined" && module.exports) {
  module.exports = partnerBrands;
} else {
  window.partnerBrands = partnerBrands;
}
"""

with open('brands.js', 'w') as f:
    f.write(js_content)

print(f"Successfully processed {len(all_brands)} brands and updated brands.js!")
