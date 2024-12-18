/* eslint-disable @typescript-eslint/no-explicit-any */

import { Applet } from '../applet';
import { AppletCapabilities } from '../AppletCapabilitiesEnum';
import { copilotParams, copilotState } from './CopilotParams';
import getTheme from './theme';
import { OSAppletEnum } from '@pieces.app/pieces-os-client';
import ConnectorSingleton from '../../../connection/connector_singleton';


export default class CopilotApplet extends Applet {
	constructor() {
		super('pieces-copilot', 'gpt-tab');
	}

	async getUrl() {
		const application = await copilotParams.getApplication();
		const baseUrl = await ConnectorSingleton.getInstance().osApi.osAppletLaunch(
			{
				inactiveOSServerApplet: {
					type: OSAppletEnum.Copilot,
					parent: application,
				},
			}
		);

		const url = new URL(`http://localhost:${baseUrl.port}`);

		const theme = getTheme();

		url.searchParams.append('theme', JSON.stringify(theme));
		url.searchParams.append('application', JSON.stringify(application));
		url.searchParams.append(
			'capabilities',
			(
				// AppletCapabilities.insertAtCursor |
				AppletCapabilities.askCopilot |
				AppletCapabilities.displayNotification |
				AppletCapabilities.persistState |
				AppletCapabilities.launchPos |
				AppletCapabilities.corsProxy |
				AppletCapabilities.setTheme |
				AppletCapabilities.addToContext |
				AppletCapabilities.copyToClipboard |
				AppletCapabilities.loaded |
				// AppletCapabilities.previewAsset |
				AppletCapabilities.openSettings |
				AppletCapabilities.focusCopilotConversation |
				AppletCapabilities.runInTerminal // Getting type = null here which is super wired!
			).toString()
		);
		if (copilotState) url.searchParams.append('state', copilotState);

		return url;
	}
}

export const copilotApplet = new CopilotApplet();

// window.addEventListener('message', handleMessage);
