import { Component } from '../../core/core.js'
import { Button } from '../Button.js'

export class CustomAlert extends Component {
  constructor(payload = {}) {
    super({
      tagName: 'div',
      props: {
        className: 'custom-alert-overlay',
      },
      ...payload
    })
    this.message = payload.message || ''
    this.okButtonText = payload.okButtonText || '확인'
    this.resolvePromise = null
  }

  render() {
    this.el.innerHTML = ''

    const alertBox = document.createElement('div')
    alertBox.className = 'custom-alert-box'

    const messageText = document.createElement('p')
    messageText.id = 'alert-message'
    messageText.className = 'custom-alert-message'
    messageText.textContent = this.message
    alertBox.appendChild(messageText)

    const okButton = new Button({
      text: this.okButtonText,
      style: 'black-alert',
      size: 'md'
    }, () => this.close())
    okButton.el.classList.add('custom-alert-button')
    alertBox.appendChild(okButton.el)

    this.el.appendChild(alertBox)

    // Focus trap
    this.el.addEventListener('keydown', this.handleKeyDown.bind(this))
  }

  handleKeyDown(event) {
    if (event.key === 'Escape') {
      this.close()
    }
  }

  close() {
    document.body.removeChild(this.el)
    if (this.resolvePromise) {
      this.resolvePromise()
    }
  }

  show() {
    return new Promise((resolve) => {
      this.resolvePromise = resolve
      document.body.appendChild(this.el)
      const okButton = this.el.querySelector('.custom-alert-button')
      okButton.focus()
    })
  }
}