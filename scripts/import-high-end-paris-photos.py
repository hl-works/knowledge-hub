#!/usr/bin/env python3
"""Download and optimize third-party reference photography for the High End Paris prototype.
Use subject to photo owner permissions; source list is intentionally explicit.
"""
from __future__ import annotations
import io
import json
import pathlib
import urllib.request
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "high-end-paris" / "assets" / "products"
OUT.mkdir(parents=True, exist_ok=True)
IMAGES = [
 ("01-focal", "https://media.focal-naim.com/dam/grande-utopia-em-evo/g_utopia_evo_green_34.jpg"),
 ("02-bowers-wilkins", "https://www.bowerswilkins.com/on/demandware.static/-/Sites-master-catalog-soundunited/default/dwd7ad5e67/bowers/PDP/801-D4/801-D4-Black/801-D4-Black_Image_1.png"),
 ("03-wilson", "https://www.definitive.com/cdn/shop/files/Alexx_v.png?v=1740421717"),
 ("04-mcintosh", "https://www.mcintoshlabs.com/-/media/images/mcintoshlabs/products/productimages/mc21kw/mc21kw-an-group-offset-front-top.jpg?rev=9f33caf991c84e86aaa799a1415bbf84&revision=9f33caf9-91c8-4e86-aaa7-99a1415bbf84"),
 ("05-accuphase", "https://www.safeandsoundhq.com/cdn/shop/files/A300-5.jpg?v=1700172849"),
 ("06-luxman", "https://unveiledaudio.com/cdn/shop/files/luxman-m-10x-1-silver.jpg?v=1760166803&width=1920"),
 ("07-dali", "https://res.cloudinary.com/dalispeakers/image/upload/v1682588807/Storyblok/Images/Products/Loudspeakers/KORE/DALI-KORE-setup_4%3A3.jpg"),
 ("08-sonus-faber", "https://stereo-box.it/cdn/shop/products/AIDA_Venge.jpg?v=1646046008&width=1240"),
 ("09-clearaudio", "https://cdn.mos.cms.futurecdn.net/CJxHVPYFZBoiTosrJ4Hmah.jpg"),
 ("10-magico", "https://nekoaudio.com/images/magico/m9_1.jpg"),
 ("11-gryphon", "https://www.auditorium.de/media/49/72/53/1770389387/auditorium-gryphon-apex-stereo-endverstaerker-294080-images-1.jpg?ts=1770389387"),
 ("12-dcs", "https://www.mirandahifi.com/cdn/shop/files/dcs-verese-system-stack-front_1500x1500_a8c3ff02-c98c-4c93-bd4d-da525d7bec0e.jpg?v=1755911424"),
 ("13-esoteric", "https://arsantiquaudio.com/5988-large_default/esoteric-grandioso-d1x-set.jpg")
]
success,fail={},{}
for slug,url in IMAGES:
    target = OUT / (slug+".webp")
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; HighEndParisGallery/1.0)","Accept":"image/avif,image/webp,image/*"})
        with urllib.request.urlopen(req, timeout=18) as resp:
            data=resp.read(12*1024*1024+1)
            if len(data)>12*1024*1024:
                raise ValueError("image exceeds limit")
        img=Image.open(io.BytesIO(data))
        img.load()
        if img.width<250 or img.height<200:
            raise ValueError(f"too small {img.size}")
        img=ImageOps.exif_transpose(img).convert("RGB")
        img.thumbnail((1200,850),Image.Resampling.LANCZOS)
        img.save(target,"WEBP",quality=83,method=6)
        success[slug]={"file":"assets/products/"+target.name,"width":img.width,"height":img.height}
        print("OK",slug,img.size,target.stat().st_size)
    except Exception as exc:
        fail[slug]=str(exc)[:240]
        print("FAIL",slug,fail[slug])
(OUT/"manifest.json").write_text(json.dumps({"images":success,"failed":fail},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
if not success:
    raise SystemExit("No product images downloaded; do not deploy empty gallery")
