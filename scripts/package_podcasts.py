#!/usr/bin/env python3
"""Package cover exports and MP3 copies, keeping original audio files untouched."""
import argparse,json,subprocess,shutil,zipfile,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def package(out):
    out=out.resolve();out.mkdir(parents=True,exist_ok=True)
    for folder in ('covers','thumbnails','mp3','portraits'):(out/folder).mkdir(exist_ok=True)
    episodes=json.loads((ROOT/'assets/podcast/episodes.json').read_text())['episodes'];manifest=[]
    for ep in episodes:
        for kind in ('short','full'):
            name=f'{ep["date"]}-{kind}';cover=ROOT/f'assets/podcast/covers/{name}.png';thumb=out/f'thumbnails-png/{name}.png'
            assert cover.is_file() and thumb.is_file()
            raw=cover.read_bytes()
            assert raw[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',raw[16:24])==(1080,1080), 'Expected a real 1080px PNG cover'
            shutil.copy2(cover,out/'covers'/cover.name)
            jpeg=out/f'thumbnails/{name}.jpg'
            subprocess.run(['ffmpeg','-y','-v','error','-i',str(thumb),'-frames:v','1','-q:v','2',str(jpeg)],check=True)
            assert jpeg.stat().st_size<200000
            label='Le Flash' if kind=='short' else 'Le Débrief';source=ROOT/ep[kind]['src'].lstrip('/');dest=out/f'mp3/{name}.mp3'
            subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-i',str(cover),'-map','0:a:0','-map','1:v:0','-c','copy','-id3v2_version','3','-metadata','artist=Le Podcast iA · Hugo Lahutte','-metadata','album=Le Podcast iA','-metadata',f'title={label} — {ep["date"]}','-metadata',f'date={ep["date"]}','-metadata:s:v','title=Album cover','-metadata:s:v','comment=Cover (front)','-disposition:v','attached_pic',str(dest)],check=True)
            data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height:stream_disposition=attached_pic:format=duration','-of','json',str(dest)]))
            assert any(s.get('disposition',{}).get('attached_pic')==1 for s in data['streams'])
            assert abs(float(data['format']['duration'])-ep[kind]['seconds'])<2
            def audio_hash(path):return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-']).decode().strip()
            assert audio_hash(source)==audio_hash(dest)
            manifest.append({'date':ep['date'],'format':label,'seconds':ep[kind]['seconds'],'audio':f'mp3/{name}.mp3','cover':f'covers/{name}.png','thumbnail':f'thumbnails/{name}.jpg','original_audio_unchanged':True,'source':ep[kind]['src']})
    for p in (ROOT/'assets/podcast/art').glob('*.png'):shutil.copy2(p,out/'portraits'/p.name)
    shutil.copy2(ROOT/'assets/podcast/art/prompts.json',out/'prompts.json')
    shutil.copy2(ROOT/'assets/podcast/art/manifest.json',out/'portraits/manifest.json')
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (out/'README.md').write_text('''# Le Podcast iA — pochettes et audios\n\n10 pochettes PNG 1080 × 1080 et 10 miniatures JPEG 320 × 320 (moins de 200 ko), avec date et durée exactes pour les éditions du 12–16 octobre 2026. Les MP3 sont des copies avec image de couverture intégrée (ID3) : leurs flux audio sont identiques aux originaux, vérifiés par hash.\n\nPortraits octobre, novembre et décembre générés avec Imagegen intégré ; prompts joints. Les dates, durées et noms sont composés en HTML/CSS, séparés des dessins. Les autres mois restent à décliner à partir du vestiaire existant.\n\nTelegram : utiliser sendAudio avec le MP3, title, performer et le JPEG associé comme thumbnail en multipart/form-data. Pour une grande vignette dans le fil, le PNG est également prêt à accompagner un message. Le rendu final dépend du client ; aucun message n’a été envoyé et le bot de production n’a pas été modifié. Documentation : https://core.telegram.org/bots/api#sendaudio\n\nNoms proposés : Le Radar iA (veille), Le Podcast iA (podcasts), iAstro Sunday (comic du dimanche). Le point d’entrée est Le Kiosque IA.\n''')
    with zipfile.ZipFile(out/'radio-iastro-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file() and (p.relative_to(out).parts[0] in ('covers','thumbnails','mp3','portraits') or p.name in ('prompts.json','manifest.json','README.md')):z.write(p,p.relative_to(out))
    print('10 pochettes, 10 JPEG, 10 MP3 illustrés ; flux audio identiques, ZIP créé.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();package(args.output)
