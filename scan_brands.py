import os
import json
import re
import shutil

brands_dir = 'BRANDS'
new_brands_dir = 'New brand entries'
images_dir = 'images'

# Copy all files from 'images' directory to root if present
if os.path.exists(images_dir):
    for f in os.listdir(images_dir):
        src = os.path.join(images_dir, f)
        if os.path.isfile(src) and not f.startswith('.'):
            shutil.copy2(src, f.lower())

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def image_sort_key(file_path):
    filename = os.path.basename(file_path)
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

def copy_and_flatten_image(img_path):
    if not img_path:
        return ""
    if img_path.startswith("images/"):
        filename = os.path.basename(img_path).lower()
    else:
        filename = re.sub(r'[^a-zA-Z0-9\._\-]', '_', img_path)
        filename = re.sub(r'_{2,}', '_', filename).lower()
        
    if os.path.exists(img_path):
        shutil.copy2(img_path, filename)
    else:
        print(f"Warning: image path does not exist: {img_path}")
    return filename

# Mapping from exact folder names to human-readable clean metadata for legacy / existing brands
brand_info_mapping = {
    " Devri updates": {
        "name": "DEVRI",
        "id": "devri",
        "monogram": "D",
        "desc": "Devri - premium cotton kurtis, chic tunics, and daily wear collections.",
        "categories": ["Kurtis", "Contemporary Styles"],
        "invite_link": "https://tr.ee/w-ooWb3Bvz"
    },
    "BUDAI EXCLUSICE UPDATES": {
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
        "monogram": "G",
        "desc": "Glamz Updates - contemporary Indo-Western styles, pre-pleated sarees, and modern fusion clothing.",
        "categories": ["Contemporary Styles", "Designer Collections"],
        "invite_link": "https://tr.ee/DWaTxJL4UB"
    },
    "GKC BRAND UPDATES": {
        "name": "GKC BRAND",
        "id": "gkc-brand",
        "monogram": "GKC",
        "desc": "GKC Brand - classic salwar suits, casual ensembles, and daily wear boutique items.",
        "categories": ["Suits", "Ethnic Wear"],
        "invite_link": "https://tr.ee/FQyRxm0wET"
    },
    "KHOOBSURAT POINT": {
        "name": "CWB BRAND SUITS",
        "id": "cwb-brand-suits",
        "monogram": "CWB",
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
        "monogram": "STO",
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
        "monogram": "Z",
        "desc": "Ziia Brand - high-end ethnic suits, elegant festive gowns, and hand-crafted designer wear.",
        "categories": ["Ethnic Wear", "Suits", "Festive Wear"],
        "invite_link": "https://tr.ee/Fx0bUgTLDm"
    }
}

# Metadata and descriptions for New Brand Entries
new_brand_meta = {
    "a to z unstiched": {
        "id": "a-to-z-unstitched",
        "name": "A TO Z UNSTITCHED",
        "monogram": "AZ",
        "description": "A to Z Unstitched - premium unstitched dress materials, fine Banarasi silk dupattas, and bespoke boutique suit sets.",
        "categories": ["Ethnic Wear", "Suits"],
        "descriptions": [
            "Unstitched royal blue silk suit fabric featuring delicate gold zari bootis and a contrast woven Banarasi dupatta.",
            "Bespoke unstitched cotton silk suit ensemble with intricate neckline thread embroidery and matching trousers.",
            "Fine unstitched boutique dress material presenting traditional handloom motifs and an artisanal zari border.",
            "Premium unstitched straight suit cut in rich festive tones, paired with a heavy floral jacquard dupatta.",
            "Elegant unstitched lawn silk collection featuring subtle ethnic patterns and a lightweight sheer dupatta.",
            "Artisanal unstitched salwar suit with gold tilla embroidery accents and coordinating tailored bottom fabric.",
            "Classic unstitched ceremonial suit piece detailed with fine resham threadwork and ornate pallu borders.",
            "Traditional unstitched summer-festive suit fabric in breathable cotton silk with contrast border details.",
            "Exclusive unstitched bridal wear suit material with heavy border embellishments and a pure silk dupatta."
        ]
    },
    "exclusive banarsi": {
        "id": "exclusive-banarasi",
        "name": "EXCLUSIVE BANARASI",
        "monogram": "EB",
        "description": "Exclusive Banarasi - royal Banarasi silk suits, hand-loomed zari brocades, and opulent ceremonial heritage ensembles.",
        "categories": ["Ethnic Wear", "Festive Wear", "Designer Collections"],
        "invite_link": "https://tr.ee/VYem35-Jl8",
        "descriptions": [
            "Royal Banarasi katan silk suit with intricate champagne gold zari bootis and an organza border dupatta.",
            "Opulent pastel Banarasi brocade suit ensemble featuring handcrafted floral jaal motifs and silk pants.",
            "Exquisite bridal Banarasi silk suit tailored with traditional shikargah patterns and woven gold selvedges.",
            "Lustrous heritage Banarasi suit set with antique silver zari weaving and a featherlight tissue dupatta.",
            "Ceremonial Banarasi silk straight suit adorned with delicate meenakari motifs and rich pallu accents.",
            "Classic royal purple Banarasi brocade suit with heavy border embroidery and coordinated solid trousers.",
            "Artisanal handloom Banarasi silk dress piece featuring geometric kadwa zari work and tasseled dupatta.",
            "Regal festive Banarasi suit in warm sunset tones, accented with detailed keri bootas and zari borders.",
            "Heritage signature Banarasi luxury ensemble combining time-honored weave techniques with modern cuts."
        ]
    },
    "nk": {
        "id": "nk-brand",
        "name": "NK BRAND",
        "monogram": "NK",
        "description": "NK Brand - regal Kashmiri-style weaves, intricate pashmina motifs, and luxury winter-festive embroidered suits.",
        "categories": ["Festive Wear", "Suits", "Ethnic Wear"],
        "invite_link": "https://tr.ee/-8ONj0vakz",
        "descriptions": [
            "Kashmiri-inspired pashmina jacquard suit with intricate multi-color paisley weaving and matching stole.",
            "Regal winter-festive woolen blend suit detailed with ornate tilla embroidery borders and solid bottoms.",
            "Luxury velvet-touch festive suit featuring traditional Kashmiri floral motifs and a woven shawl dupatta.",
            "Sophisticated straight suit in rich jewel tones, accented with detailed jamawar weaving and soft trousers.",
            "Artisanal Kashmiri print salwar suit with contrast border piping and an elegant coordinating stole.",
            "Boutique winter collection suit presenting fine needlework embroidery panels and warm woven fabric.",
            "Contemporary ethnic suit featuring Kashmiri kashida threadwork and an ultra-soft woven wrap.",
            "Exclusive designer winter suit with gold thread highlights and a rich patterned winter stole.",
            "Traditional ceremonial Kashmiri suit set with all-over jaal embroidery and matching woven dupatta."
        ]
    },
    "pc": {
        "id": "pc-brand",
        "name": "PC BRAND",
        "monogram": "PC",
        "description": "PC Brand - artisanal Bandhani tie-dye suits, shimmer crushed fabrics, and vibrant wedding couture.",
        "categories": ["Designer Collections", "Festive Wear", "Ethnic Wear"],
        "invite_link": "https://tr.ee/Wrw7SisBda",
        "descriptions": [
            "Artisanal mustard Bandhani tie-dye suit on lustrous silk with shimmer crushed gold border and tassel trim.",
            "Vibrant traditional Bandhej festive suit featuring delicate gota patti highlights and solid coordinates.",
            "Designer crushed georgette suit set with hand-tied Bandhani dots and a glistening metallic border.",
            "Opulent wedding guest ensemble with rich Bandhani print dupatta and mirror-accented neckline.",
            "Contemporary Bandhej straight suit styled with delicate pearl drops and a flowing lightweight dupatta.",
            "Festive bridal Bandhani suit in crimson and gold, embellished with intricate threadwork borders.",
            "Chic partywear suit set featuring dual-tone Bandhani patterns and a coordinating shimmer dupatta.",
            "Traditional Rajasthani Bandhej suit tailored in breathable modal silk with fine golden fringes.",
            "Signature PC couture Bandhani creation presenting heritage resist-dye techniques with modern flair."
        ]
    },
    "ps": {
        "id": "ps-brand",
        "name": "PS BRAND",
        "monogram": "PS",
        "description": "PS Brand - exquisite raw silk suits with heavy border embroidery, hand-finished zardozi, and festive silhouettes.",
        "categories": ["Suits", "Festive Wear", "Ethnic Wear"],
        "invite_link": "https://tr.ee/G8BLPA0fN2",
        "descriptions": [
            "Heavy embroidered raw silk suit in deep ochre, decorated with contrast black and gold zari border work.",
            "Luxury boutique festive suit set with intricate cutwork zardozi on neckline and hemline.",
            "Elegant raw silk ceremonial suit featuring fine thread embroidery panels and an organza dupatta.",
            "Designer partywear suit with rich antique border detailing, paired with solid trousers and dupatta.",
            "Royal evening salwar suit adorned with sequin work and metallic resham embroidery.",
            "Artisanal hand-embroidered suit set with scallop borders and matching embellished dupatta.",
            "Festive straight suit in jewel tones, detailed with delicate mirror accents and luxury fabric.",
            "Boutique wedding collection suit presenting intricate bootis and a contrast woven silk dupatta.",
            "Signature PS luxury ensemble with heavy bridal zardozi borders and coordinated bottom fabric."
        ]
    },
    "SC": {
        "id": "sc-brand",
        "name": "SC BRAND",
        "monogram": "SC",
        "description": "SC Brand - high-fashion floral designer ensembles, digital printed suits, and contemporary boutique silhouettes.",
        "categories": ["Suits", "Contemporary Styles", "Designer Collections"],
        "invite_link": "https://tr.ee/7X7j7mZIWq",
        "descriptions": [
            "High-fashion pastel floral suit with intricate tassel neck cords and a digital printed chiffon dupatta.",
            "Contemporary designer straight suit with botanical prints, tailored cuts, and matching solid trousers.",
            "Chic boutique partywear suit in fresh seasonal colors with delicate lace hem accents.",
            "Artisanal printed lawn suit set featuring modern watercolor florals and an airy organza dupatta.",
            "Sophisticated ethnic tunic suit with subtle gold foil highlights and comfortable tailored bottoms.",
            "Modern Indo-Western fusion suit presenting stylized floral patterns and lightweight dupatta.",
            "Designer pastel suit set adorned with minimal threadwork and statement printed borders.",
            "Elegant daily luxury suit tailored in breathable fine cotton with contemporary sleeve details.",
            "Signature SC designer lookbook creation with artistic prints and sweeping luxury dupatta drape."
        ]
    },
    "SDT": {
        "id": "sdt-brand",
        "name": "SDT BRAND",
        "monogram": "SD",
        "description": "SDT Brand - luxury metallic brocade suits, royal jacquard weaves, and regal ceremonial occasion wear.",
        "categories": ["Ethnic Wear", "Festive Wear", "Suits"],
        "invite_link": "https://tr.ee/-urVFko4V9",
        "descriptions": [
            "Regal charcoal and antique gold metallic jacquard suit with ornate yoke work and matching woven cape dupatta.",
            "Royal brocade ceremonial suit set featuring intricate geometric weaves and coordinated trousers.",
            "Opulent festive suit in rich metallic sheen, detailed with heritage motifs and solid silk pants.",
            "Sophisticated luxury partywear suit with subtle gold sheen weaving and delicate tassel finishes.",
            "Boutique festive jacquard ensemble presenting rich luster and an elegant draped tissue dupatta.",
            "Ceremonial straight-cut suit tailored in heavy jacquard with fine metallic resham borders.",
            "Artisanal woven festive suit set in deep regal tones, ideal for winter wedding celebrations.",
            "Luxury metallic jacquard suit with scalloped dupatta borders and tailored pencil trousers.",
            "Signature SDT royal collection suit showcasing heirloom-quality weaves and bespoke tailoring."
        ]
    }
}

# 1. Load existing base brands from brands.js to ensure no loss of existing catalog data
retained_existing_brands = []
new_brand_ids = {meta["id"] for meta in new_brand_meta.values()}

if os.path.exists('brands.js'):
    with open('brands.js', 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'const partnerBrands = (\[[\s\S]*?\]);\s*//', content)
    if not match:
        match = re.search(r'const partnerBrands = (\[[\s\S]*?\]);', content)
    if match:
        existing_brands = json.loads(match.group(1))
        for b in existing_brands:
            if b["id"] not in new_brand_ids:
                retained_existing_brands.append(b)

# 2. Process New Brand Entries if folder exists
processed_new_brands = []
if os.path.exists(new_brands_dir):
    folder_names = sorted([d for d in os.listdir(new_brands_dir) if os.path.isdir(os.path.join(new_brands_dir, d)) and not d.startswith(".")])
    
    for folder in folder_names:
        folder_path = os.path.join(new_brands_dir, folder)
        info = new_brand_meta.get(folder, {})
        
        brand_id = info.get("id", folder.lower().strip().replace(' ', '-'))
        display_name = info.get("name", folder.strip().upper())
        monogram = info.get("monogram", folder[:2].upper())
        brand_desc = info.get("description", f"{display_name} - curated women\'s fashion collections.")
        categories = info.get("categories", ["Suits", "Ethnic Wear"])
        post_descriptions = info.get("descriptions", [
            f"Exclusive design collection piece from {display_name} lookbook." for _ in range(9)
        ])
        
        subdirs = sorted([
            s for s in os.listdir(folder_path) 
            if os.path.isdir(os.path.join(folder_path, s)) and not s.startswith(".")
        ], key=natural_sort_key)
        
        subdir_images = {}
        for s in subdirs:
            spath = os.path.join(folder_path, s)
            imgs = sorted([
                os.path.join(spath, f) for f in os.listdir(spath)
                if not f.startswith(".") and f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
            ], key=image_sort_key)
            subdir_images[s] = imgs
            
        posts = []
        for post_idx in range(9):
            post_num = post_idx + 1
            desc = post_descriptions[post_idx]
            
            # Select 3 images for this post
            if folder == "exclusive banarsi":
                f_map = {
                    0: (subdirs[0], [0, 1, 2]),
                    1: (subdirs[0], [3, 4, 5]),
                    2: (subdirs[1], [0, 1, 2]),
                    3: (subdirs[1], [3, 4, 0]),
                    4: (subdirs[2], [0, 1, 2]),
                    5: (subdirs[2], [3, 4, 5]),
                    6: (subdirs[3], [0, 1, 2]),
                    7: (subdirs[3], [3, 4, 5]),
                    8: ("highlight", [subdir_images[subdirs[0]][0], subdir_images[subdirs[1]][0], subdir_images[subdirs[2]][0]])
                }
                if post_idx == 8:
                    selected_raw_imgs = f_map[post_idx][1]
                else:
                    target_s, indices = f_map[post_idx]
                    available = subdir_images[target_s]
                    selected_raw_imgs = [available[i % len(available)] for i in indices]
            elif folder == "SC" and post_idx == 4:
                # Subdir 5 is empty; use images from Subdir 1 [3:6]
                available = subdir_images[subdirs[0]]
                selected_raw_imgs = available[3:6]
            else:
                target_s = subdirs[post_idx % len(subdirs)]
                available = subdir_images.get(target_s, [])
                if not available:
                    available = subdir_images[subdirs[0]]
                if len(available) == 1:
                    selected_raw_imgs = [available[0], available[0], available[0]]
                elif len(available) == 2:
                    selected_raw_imgs = [available[0], available[1], available[0]]
                else:
                    selected_raw_imgs = available[:3]
                    
            # Flatten and copy images
            flattened_images = [copy_and_flatten_image(img_path) for img_path in selected_raw_imgs]
            
            wa_message = f"Hello A to Z a Khoobsurat Point, I am inquiring about a style from the digital lookbook.%0A%0A" \
                         f"*Brand:* {display_name}%0A" \
                         f"*Item:* Post %23{post_num}%0A" \
                         f"*Description:* {desc}"
            whatsapp_url = f"https://wa.me/918874200694?text={wa_message.replace(' ', '%20')}"
            
            posts.append({
                "id": f"{brand_id}-post-{post_num}",
                "number": post_num,
                "images": flattened_images,
                "description": desc,
                "whatsappUrl": whatsapp_url
            })
            
        previews = [posts[i]["images"][0] for i in range(min(3, len(posts)))]
        brand_join_url = info.get("invite_link", f"https://wa.me/918874200694?text=Hello%20A%20to%20Z%20a%20Khoobsurat%20Point,%20I%20am%20interested%20in%20joining%20updates%20for%20{display_name.replace(' ', '%20')}.")
        
        processed_new_brands.append({
            "id": brand_id,
            "name": display_name,
            "monogram": monogram,
            "description": brand_desc,
            "categories": categories,
            "whatsappUrl": brand_join_url,
            "previews": previews,
            "posts": posts
        })
        print(f"Processed brand: {display_name} with {len(posts)} posts")

all_brands = retained_existing_brands + processed_new_brands

# Output JS content
js_content = f"const partnerBrands = {json.dumps(all_brands, indent=2)};\n\n"
js_content += """// Export to make it accessible in index.js and brand.js
if (typeof module !== "undefined" && module.exports) {
  module.exports = partnerBrands;
} else {
  window.partnerBrands = partnerBrands;
}
"""

with open('brands.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully processed {len(all_brands)} total partner brands in brands.js!")
