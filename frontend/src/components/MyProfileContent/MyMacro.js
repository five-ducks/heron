import { Component } from "../../core/core.js";
import { Input } from "../../components/Input/Input.js";

export class MyMacro extends Component {
	constructor(props) {
		super({
			props: {
				className: 'my-macro row',
			}
		});
		this.macroTextRender(props);
	}
	macroTextRender(macroText) {
		const f1 = new Input({
            variant: 'background',
            id: 'f1',
			size: 'l',
			defaultValue: macroText[0],
            label: 'f1',
			labelPosition: 'left',
        });
		const f2 = new Input({
            variant: 'background',
            id: 'f2',
			size: 'l',
			defaultValue: macroText[1],
            label: 'f2',
			labelPosition: 'left',
        });

		const f3 = new Input({
            variant: 'background',
            id: 'f3',
			size: 'l',
			defaultValue: macroText[2],
            label: 'f3',
			labelPosition: 'left',
        });

		const f4 = new Input({
            variant: 'background',
            id: 'f4',
			size: 'l',
			defaultValue: macroText[3],
            label: 'f4',
			labelPosition: 'left',
        });

		const f5 = new Input({
            variant: 'background',
            id: 'f5',
			size: 'l',
			defaultValue: macroText[4],
            label: 'f5',
			labelPosition: 'left',
        });

		f1.el.classList.add('input-macro', 'col-12');
		f2.el.classList.add('input-macro', 'col-12');
		f3.el.classList.add('input-macro', 'col-12');
		f4.el.classList.add('input-macro', 'col-12');
		f5.el.classList.add('input-macro', 'col-12');
		
		this.el.appendChild(f1.el);
		this.el.appendChild(f2.el);
		this.el.appendChild(f3.el);
		this.el.appendChild(f4.el);
		this.el.appendChild(f5.el);
	}
}