#include <QCoreApplication>
#include <QSignalSpy>
#include <QtTest>

// add necessary includes here
#include "bscintillaedit.h"

class TestBScintillaEdit : public QObject
{
    Q_OBJECT

public:
    TestBScintillaEdit() {}
    ~TestBScintillaEdit() {}

private slots:
    void test_textChanged();
};


void TestBScintillaEdit::test_textChanged()
{
    auto editor = new BScintillaEdit();
    auto spy = QSignalSpy(editor, &BScintillaEdit::textChanged);

    // nothing really changes from the default value so no signal should be emitted
    editor->setText("");
    QCOMPARE(spy.count(), 0);

    // set the text programatically
    editor->setText("foo");
    QCOMPARE(spy.count(), 1);
    auto args = spy.takeFirst();
    QCOMPARE(args.at(0).toString(), QString("foo"));

    // clear the widget
    editor->clear();
    QCOMPARE(spy.count(), 1);
    args = spy.takeFirst();
    QCOMPARE(args.at(0).toString(), QString(""));

    // enter some text interactively
    auto inner_widget = editor->findChild<QWidget*>("scintilla_base_edit");
    QVERIFY(inner_widget != nullptr);
    auto text = QString("hello world");
    QTest::keyClicks(inner_widget, text);

    // the signal is emitted every time a key is pressed
    QCOMPARE(spy.count(), text.size());

    // the first signal is emitted with the first char from the test text
    args = spy.takeFirst();
    QCOMPARE(args.at(0).toString(), text.at(0));

    // the last signal is emitted with the full text
    args = spy.takeLast();
    QCOMPARE(args.at(0).toString(), text);
}


QTEST_MAIN(TestBScintillaEdit)

#include "tst_bscintillaedit.moc"
