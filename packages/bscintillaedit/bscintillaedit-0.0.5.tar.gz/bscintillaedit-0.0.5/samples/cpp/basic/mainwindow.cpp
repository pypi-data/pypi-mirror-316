#include "mainwindow.h"
#include "./ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    auto editor = ui->bScintillaEdit;
    auto viewer = ui->textBrowser;

    connect(editor, &BScintillaEdit::textChanged, viewer, &QTextBrowser::setText);

    auto action = ui->actionToggleLineEndVisibility;
    connect(
        action, &QAction::toggled,
        editor, &BScintillaEdit::setLineEndVisible
        );
    editor->setLineEndVisible(action->isChecked());

    action = ui->actionToggleLineNumberVisibility;
    connect(
        action, &QAction::toggled,
        editor, &BScintillaEdit::setLineNumbersVisible
        );
    editor->setLineNumbersVisible(action->isChecked());

    action = ui->actionToggleLineWrapping;
    connect(
        action, &QAction::toggled,
        editor, &BScintillaEdit::setLineWrapped
        );
    editor->setLineWrapped(action->isChecked());

    action = ui->actionToggleReadOnly;
    connect(
        action, &QAction::toggled,
        editor, &BScintillaEdit::setReadOnly
        );
    editor->setReadOnly(action->isChecked());

    editor->setText(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque vulputate id purus "
        "eu porta. Donec ut massa quis mi accumsan tempus. In hac habitasse platea dictumst. Donec "
        "interdum, nulla at lacinia gravida, augue ante dictum dui, ac congue lectus urna eu massa."
        "\n\n"
        "Maecenas eget elementum arcu. Nunc sit amet nisl leo. Nullam bibendum ac enim sit amet "
        "vestibulum."
        );
}

MainWindow::~MainWindow()
{
    delete ui;
}
