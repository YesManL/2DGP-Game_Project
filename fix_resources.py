import os
import re

# 수정할 파일 리스트
files_to_modify = [
    'player.py', 'enemy.py', 'bullet.py', 'item.py', 'explosion.py',
    'ui.py', 'title_mode.py', 'shop_mode.py', 'gameover_mode.py',
    'upgrade_mode.py', 'play_mode.py', 'minimap.py'
]

def add_resource_path(filepath):
    if not os.path.exists(filepath):
        print(f"Skip: {filepath} (not found)")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 이미 resource_path import가 있으면 스킵
    if 'from resource_path import resource_path' in content:
        print(f"Skip: {filepath} (already has resource_path)")
        return

    # import 섹션 찾기
    lines = content.split('\n')
    import_end = 0
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            import_end = i + 1

    # resource_path import 추가
    lines.insert(import_end, 'from resource_path import resource_path')

    # 전체 내용 결합
    content = '\n'.join(lines)

    # load_image, load_wav, load_music에 resource_path 적용
    content = re.sub(r"load_image\('([^']+)'\)", r"load_image(resource_path('\1'))", content)
    content = re.sub(r'load_image\("([^"]+)"\)', r'load_image(resource_path("\1"))', content)
    content = re.sub(r"load_wav\('([^']+)'\)", r"load_wav(resource_path('\1'))", content)
    content = re.sub(r'load_wav\("([^"]+)"\)', r'load_wav(resource_path("\1"))', content)
    content = re.sub(r"load_music\('([^']+)'\)", r"load_music(resource_path('\1'))", content)
    content = re.sub(r'load_music\("([^"]+)"\)', r'load_music(resource_path("\1"))', content)

    # f-string 내부의 경로도 처리
    content = re.sub(r"load_image\(f'([^']+)'\)", r"load_image(resource_path(f'\1'))", content)
    content = re.sub(r'load_image\(f"([^"]+)"\)', r'load_image(resource_path(f"\1"))', content)

    # 중복 resource_path 제거 (resource_path(resource_path(...)))
    content = re.sub(r'resource_path\(resource_path\(([^)]+)\)\)', r'resource_path(\1)', content)

    # 파일 저장
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Modified: {filepath}")

# 모든 파일 수정
for filename in files_to_modify:
    add_resource_path(filename)

print("\nAll files processed!")

