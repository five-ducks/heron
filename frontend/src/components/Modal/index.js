import { Component } from "../../core/core.js";

export class Modal extends Component {
    constructor(title, content = '', onClose = () => { }) {
        super({
            tagName: 'div',
            props: {
                // Bootstrap 클래스로 변경
                className: 'modal fade show'
            }
        });
        this.el.innerHTML = /*html*/`
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">${content}</div>
                </div>
            </div>
        `;

        this.onClose = onClose;
        // 클래스 선택자 변경
        this.el.querySelector('.btn-close').addEventListener('click', () => {
            this.close();
        });

        // 이벤트 위임을 사용하여 코드 간소화
        this.el.addEventListener('click', (event) => {
            if (event.target === this.el) {
                this.close();
            }
        });
    }

    open() {
        // Bootstrap 클래스와 인라인 스타일 사용
        this.el.style.display = 'block';
        this.el.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        document.body.classList.add('modal-open');
        history.pushState(null, "", location.href);
        window.addEventListener("popstate", this.preventGoBack);
    }

    close() {
        this.el.style.display = 'none';
        document.body.classList.remove('modal-open');
        window.removeEventListener("popstate", this.preventGoBack);
        this.onClose();
        this.el.remove();
    }

    preventGoBack() {
        history.go(1);
    }
}