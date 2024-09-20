import os

def merge_files_to_md(directory_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as md_file:
        # 디렉터리 내 모든 파일 순회
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                
                # 파일 확장자 추출
                file_extension = os.path.splitext(file_name)[1]
                
                # 파일 경로와 확장자를 마크다운 형식으로 추가
                md_file.write(f"### {file_path}\n")
                md_file.write(f"```{file_extension}\n")
                
                # 파일 내용 읽기
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                    md_file.write(file_content)
                
                # 마크다운 종료 구문 추가
                md_file.write("\n```\n\n")

# 사용 예시
merge_files_to_md('/Users/seokjyan/Desktop/tcen/frontend/src/components/GameRecords', './mds/q.md')