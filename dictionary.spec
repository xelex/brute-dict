require './dictionary'
require 'rspec'

RSpec.describe "Dictionary" do
  it "Corner cases" do
    expect(Dictionary.new(abc: "", len: 1).total).to eq 0
    expect(Dictionary.new(abc: "1", len: 1).total).to eq 1
    expect(Dictionary.new(abc: "123", len: 0).total).to eq 1
    expect(Dictionary.new(abc: "123", len: 0).next(1).first).to eq ""
    expect(Dictionary.new(abc: "123", len: 1).next(0).count).to eq 0
  end

  it "Single char alphabet" do
    expect(Dictionary.new(abc: "1", len: 6).total).to eq 1
    expect(Dictionary.new(abc: "1", len: 6).next(1).count).to eq 1
    expect(Dictionary.new(abc: "1", len: 6).next(100).count).to eq 1
    expect(Dictionary.new(abc: "1", len: 6).next(1).first).to eq "111111"
  end

  it "Iterator usage" do
    tmp = Dictionary.new(abc: "12", len: 1)
    expect(tmp.total).to eq 2
    expect(tmp.next(1).count).to eq 1
    expect(tmp.next(1).count).to eq 1
    expect(tmp.next(1).count).to eq 0
    expect(tmp.next(100).count).to eq 0
    tmp.reset
    expect(tmp.next(1).count).to eq 1
    expect(tmp.next(1).count).to eq 1
    expect(tmp.next(1).count).to eq 0
    expect(tmp.next(100).count).to eq 0
    tmp.reset
    expect(tmp.next(100).count).to eq 2

    expect(Dictionary.new(abc: "12", len: 1).next(100).count).to eq 2
  end

  it "Simple usage" do
    expect(Dictionary.new(abc: "12", len: 1).total).to eq 2
    expect(Dictionary.new(abc: "12", len: 1).next(100).count).to eq 2
    expect(Dictionary.new(abc: "12", len: 1).next(100).sort).to eq ["1", "2"]

    expect(Dictionary.new(abc: "12", len: 2).total).to eq 4
    expect(Dictionary.new(abc: "12", len: 2).next(100).count).to eq 4
    expect(Dictionary.new(abc: "12", len: 2).next(100).sort).to eq ["1", "2"].repeated_permutation(2).map {|v| v.join}

    expect(Dictionary.new(abc: "123", len: 2).total).to eq 9
    expect(Dictionary.new(abc: "123", len: 2).next(100).count).to eq 9
    expect(Dictionary.new(abc: "123", len: 2).next(100).sort).to eq ["1", "2", "3"].repeated_permutation(2).map {|v| v.join}
  end

  it "Filter usage" do
    expect(Dictionary.new(abc: "123", len: 2).match(/^1.$/).total).to eq 9
    expect(Dictionary.new(abc: "123", len: 2).match(/^1.$/).next(100).count).to eq 3
    expect(Dictionary.new(abc: "123", len: 2).match(/^1.$/).next(100).sort).to eq ["11", "12", "13"]

    expect(Dictionary.new(abc: "123", len: 2).nomatch(/^1.$/).total).to eq 9
    expect(Dictionary.new(abc: "123", len: 2).nomatch(/^1.$/).next(100).count).to eq 6
    expect(Dictionary.new(abc: "123", len: 2).nomatch(/^1.$/).next(100).sort).to eq ["21", "22", "23", "31", "32", "33"]
  end
end