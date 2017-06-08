import { AppuiPage } from './app.po';

describe('appui App', () => {
  let page: AppuiPage;

  beforeEach(() => {
    page = new AppuiPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
