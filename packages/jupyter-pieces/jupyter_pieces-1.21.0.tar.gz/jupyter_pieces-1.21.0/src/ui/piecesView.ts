import { JupyterFrontEnd } from '@jupyterlab/application';
import { Widget } from '@lumino/widgets';
import createAsset from './../actions/create_asset';
import Constants from '../const';
import { SegmentAnalytics } from '../analytics/SegmentAnalytics';
import { AnalyticsEnum } from '../analytics/AnalyticsEnum';
import PiecesCacheSingleton from '../cache/pieces_cache';
import { renderNavBar } from './render/renderSearchBox';
import { PiecesLogo } from './LabIcons';
import { snippetApplet } from './views/snippets';
import { copilotApplet } from './views/copilot';
import { handleOnMessage } from './views/messageHandler';

export class PiecesView {
  private app: any;
  private viewWidget: Widget;
  private navTab!: Element;
  private parentDiv!: HTMLDivElement;
  private snippetsTab!: HTMLDivElement;
  private gptTab!: HTMLDivElement;
  cache = PiecesCacheSingleton.getInstance();
  currentTab: Element | undefined = undefined;

  constructor() {
    this.viewWidget = new Widget();
  }

  public async build(app: JupyterFrontEnd): Promise<void> {
    this.app = app;

    await this.createView();
    this.prepareRightClick();
  }

  private saveSelection(): void {
    SegmentAnalytics.track({
      event: AnalyticsEnum.JUPYTER_SAVE_SELECTION,
    });

    const notebookName = this.app.shell.currentPath ?? 'unknown';
    createAsset({
      selection: this.app.Editor.selection,
      filePath: notebookName === 'unknown' ? undefined : notebookName,
    });
  }

  private prepareRightClick(): void {
    const command = 'jupyter_pieces:menuitem';

    this.app.commands.addCommand(command, {
      label: 'Save to Pieces',
      execute: () => this.saveSelection(), // Fixed to bind correct this context
    });

    this.app.contextMenu.addItem({
      command: command,
      selector: '.jp-CodeCell-input .jp-Editor .jp-Notebook *',
      rank: 100,
    });
  }

  private async createView() {
    this.viewWidget.id = 'piecesView';
    this.viewWidget.title.closable = true;
    this.viewWidget.title.icon = PiecesLogo;

    const containerVar = this.viewWidget.node;
    containerVar.remove();

    const wrapper = renderNavBar({ containerVar: containerVar });
    this.navTab = wrapper.children[0];
    this.currentTab = this.navTab.children[1];

    this.parentDiv = document.createElement('div');
    this.parentDiv.classList.add('parent-div-container', 'w-full');
    this.parentDiv.id = 'pieces-parent';
    containerVar.appendChild(this.parentDiv);

    this.snippetsTab = document.createElement('div');
    this.snippetsTab.classList.add('px-2', 'w-full', 'pt-8');
    this.snippetsTab.id = 'snippets-tab';
    this.parentDiv.appendChild(this.snippetsTab);

    this.gptTab = document.createElement('div');
    this.gptTab.classList.add('px-2', 'w-full', 'pt-8');
    this.gptTab.id = 'gpt-tab';
    this.parentDiv.appendChild(this.gptTab);

    snippetApplet.init(this.snippetsTab);
    copilotApplet.init(this.gptTab);
    window.addEventListener('message', handleOnMessage);

    this.navTab.addEventListener('click', (event) => {
      this.changeViews(event);
    });

    if ((this.navTab.children[0] as HTMLInputElement).checked) {
      this.gptTab.style.display = 'none';
    } else if ((this.navTab.children[2] as HTMLInputElement).checked) {
      this.parentDiv.classList.add('gpt-parent');
      this.snippetsTab.style.display = 'none';
    }

    this.app.shell.add(this.viewWidget, 'right', { rank: 1 });
  }

  public switchTab(tabName: 'snippets' | 'gpt') {
    if (tabName === 'snippets') {
      (this.navTab.children[0] as HTMLInputElement).checked = true;
      (this.navTab.children[2] as HTMLInputElement).checked = false;
      this.currentTab = this.navTab.children[1];

      this.parentDiv.classList.remove('gpt-parent');
      this.gptTab.style.display = 'none';
      this.snippetsTab.style.display = 'flex';

      Constants.PIECES_CURRENT_VIEW = AnalyticsEnum.JUPYTER_VIEW_SNIPPET_LIST;
    } else if (tabName === 'gpt') {
      (this.navTab.children[0] as HTMLInputElement).checked = false;
      (this.navTab.children[2] as HTMLInputElement).checked = true;
      this.currentTab = this.navTab.children[3];

      this.parentDiv.classList.add('gpt-parent');
      this.snippetsTab.style.display = 'none';
      this.gptTab.style.display = 'flex';

      Constants.PIECES_CURRENT_VIEW = AnalyticsEnum.JUPYTER_VIEW_CHATBOT;
    }
  }

  private changeViews(event: Event) {
    if (event.target !== this.currentTab) {
      if (event.target === this.navTab.children[1]) {
        this.switchTab('snippets');
      } else if (event.target === this.navTab.children[3]) {
        this.switchTab('gpt');
      }
    }
  }
}
