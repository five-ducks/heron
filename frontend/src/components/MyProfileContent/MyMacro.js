import { Component } from "../../core/core.js";
import { Input } from "../../components/Input/Input.js";

export class MyMacro extends Component {
	constructor(props) {
		super({
			props: {
				className: 'my-macro',
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
        });
		const f2 = new Input({
            variant: 'background',
            id: 'f2',
			size: 'l',
			defaultValue: macroText[1],
            label: 'f2',
        });

		const f3 = new Input({
            variant: 'background',
            id: 'f3',
			size: 'l',
			defaultValue: macroText[2],
            label: 'f3',
        });

		const f4 = new Input({
            variant: 'background',
            id: 'f4',
			size: 'l',
			defaultValue: macroText[3],
            label: 'f4',
        });

		const f5 = new Input({
            variant: 'background',
            id: 'f5',
			size: 'l',
			defaultValue: macroText[4],
            label: 'f5',
        });
		this.el.appendChild(f1.el);
		this.el.appendChild(f2.el);
		this.el.appendChild(f3.el);
		this.el.appendChild(f4.el);
		this.el.appendChild(f5.el);
	}
}